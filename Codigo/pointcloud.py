import sim
import numpy as np
import math
import open3d as o3d
import matplotlib.pyplot as plt
import pyransac3d as pyrsc
import cv2

def draw_guild_lines(dic, density = 0.01):
        x_start,x_end = dic["x"]
        y_start,y_end = dic["y"]
        z_start,z_end = dic["z"]

        x_points,y_points,z_points = np.asarray(np.arange(x_start,x_end,density)),np.asarray(np.arange(y_start,y_end,density)),np.asarray(np.arange(z_start,z_end,density))

        y_starts,y_ends = np.asarray(np.full((len(x_points)),y_start)),np.asarray(np.full((len(x_points)),y_end))
        z_starts,z_ends = np.asarray(np.full((len(x_points)),z_start)),np.asarray(np.full((len(x_points)),z_end))
        lines_x = np.concatenate((np.vstack((x_points,y_starts,z_starts)).T,np.vstack((x_points,y_ends,z_starts)).T,np.vstack((x_points,y_starts,z_ends)).T,np.vstack((x_points,y_ends,z_ends)).T))


        x_starts,x_ends = np.asarray(np.full((len(y_points)),x_start)),np.asarray(np.full((len(y_points)),x_end))
        z_starts,z_ends = np.asarray(np.full((len(y_points)),z_start)),np.asarray(np.full((len(y_points)),z_end))
        lines_y = np.concatenate((np.vstack((x_starts,y_points,z_starts)).T,np.vstack((x_ends,y_points,z_starts)).T,np.vstack((x_starts,y_points,z_ends)).T,np.vstack((x_ends,y_points,z_ends)).T))


        x_starts,x_ends = np.asarray(np.full((len(z_points)),x_start)),np.asarray(np.full((len(z_points)),x_end))
        y_starts,y_ends = np.asarray(np.full((len(z_points)),y_start)),np.asarray(np.full((len(z_points)),y_end))
        lines_z = np.concatenate((np.vstack((x_starts,y_starts,z_points)).T,np.vstack((x_ends,y_starts,z_points)).T,np.vstack((x_starts,y_ends,z_points)).T,np.vstack((x_ends,y_ends,z_points)).T))

        lines_x_color = np.zeros((len(lines_x),3))
        lines_y_color = np.zeros((len(lines_y),3))
        lines_z_color = np.zeros((len(lines_z),3))

        lines_x_color[:,0] = 1.0 #red for x
        lines_y_color[:,1] = 1.0 #green for y
        lines_z_color[:,2] = 1.0 #blue for z
        return np.concatenate((lines_x,lines_y,lines_z)),np.asmatrix(np.concatenate((lines_x_color,lines_y_color,lines_z_color)))

def pass_through_filter(dic, aux_xyzv):
    xbool=aux_xyzv[0]>=dic["x"][0] and aux_xyzv[0]<=dic["x"][1]
    ybool=aux_xyzv[1]>=dic["y"][0] and aux_xyzv[1]<=dic["y"][1]
    zbool=aux_xyzv[2]>=dic["z"][0] and aux_xyzv[2]<=dic["z"][1]
    return (xbool and ybool and zbool)

def Get_Image(sensorHandle, robot, angulo, visualizar):
    retCode, resolution, imaged=sim.simxGetVisionSensorDepthBuffer(robot.clientID, sensorHandle,sim.simx_opmode_oneshot_wait)
    retCode, resolution, image=sim.simxGetVisionSensorImage(robot.clientID,sensorHandle,0,sim.simx_opmode_oneshot_wait)
    img = np.absolute(np.array(image)).astype(np.float32)
    img.resize([resolution[1], resolution[0], 3])
    img = (np.flipud(img)) / 255.0
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    imgd= np.array(imaged)
    imgd.resize([resolution[1],resolution[0]])
    imgd=np.flipud(imgd)
    imgdaux=imgd.flatten()
    u_res=resolution[1]
    v_res=resolution[0]
    near_clip=0.01
    far_clip=3.5
    xyzv=np.array([])
    focal_length = (640.0/2.0) / math.tan((83.0/2.0) * np.pi/ 180)
    ss = math.sin(math.radians(angulo))
    cs = math.cos(math.radians(angulo))
    centers = np.array([])
    dic = {"x":[-1,2], #rojo
           "z":[0.025,1], #azul
            "y":[-1.75,1.75]} #verde
    for u in range(u_res):
        for v in range(v_res):
                w = int(v_res * u + v)
                y =  far_clip * imgdaux[w] + near_clip
                z = (-(u - u_res / 2.0) * y / focal_length)+0.6
                x = (v - v_res / 2.0) * y / focal_length
                aux_xyzv=np.array([(x*cs-y*ss), (x*ss+y*cs), z])
                if pass_through_filter(dic, aux_xyzv):  #pass through filter
                    auxhsv=[img[u][v][0]/360.0,img[u][v][2],img[u][v][1]]
                    if ((auxhsv[0] < 0.20 or auxhsv[0] > 0.97) and auxhsv[1] > 0.60 and auxhsv[2] > 0.23): #Threshold HSI
                        xyzv = np.append(xyzv, aux_xyzv)
    if len(xyzv) != 0:
        xyzv=np.reshape(xyzv,(-1,3))
        pcl = o3d.geometry.PointCloud()
        pcl.points = o3d.utility.Vector3dVector(xyzv)
        labels = np.array(pcl.cluster_dbscan(eps=0.05, min_points=20))  #Clustering
        if  labels.size!=0:
            max_label = labels.max()
            colors = plt.get_cmap("tab20")(labels / (max_label))
            colors[labels < 0] = 0
            pcl.colors = o3d.utility.Vector3dVector(colors[:, :3])
            if visualizar:
                new_pos, new_col = draw_guild_lines(dic)
                guild_points = o3d.geometry.PointCloud()
                guild_points.points = o3d.utility.Vector3dVector(new_pos)
                guild_points.colors = o3d.utility.Vector3dVector(new_col)
                vis = o3d.visualization.Visualizer()
                vis.create_window(width=960,height=540)
                vis.add_geometry(pcl)
                vis.add_geometry(guild_points)

            for i in range(max_label+1):  #Ransac each label
                  points = np.asarray(pcl.points)[labels==i]
                  sph = pyrsc.Sphere()
                  center, radius, inliers = sph.fit(points, thresh=0.01)
                  if pass_through_filter(dic, center) and radius<=0.1 and radius>=0.01:
                      centers = np.append(centers, center)
                      sphere=o3d.geometry.TriangleMesh.create_sphere(radius)
                      sphere.paint_uniform_color(np.asarray(pcl.colors)[labels==i][0])
                      sphere=sphere.translate(center)
                      if visualizar:
                          vis.add_geometry(sphere)
            centers=np.reshape(centers,(-1,3))
            if visualizar:
                vis.get_view_control()
                vis.run()
    return centers

