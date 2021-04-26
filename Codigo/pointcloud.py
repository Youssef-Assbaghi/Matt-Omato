import sim
import numpy as np
import math
import cv2                      # opencv
import matplotlib.pyplot as plt # pyplot
import open3d as o3d

def connect(port):
# Establece la conexión a COPPELIA
# El port debe coincidir con el puerto de conexión en VREP  -- DALE AL PLAY !!!
# retorna el número de cliente o -1 si no puede establecer conexión
    sim.simxFinish(-1) # just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',port,True,True,2000,5) # Conectarse
    if clientID == 0: print("conectado a", port)
    else: print("no se pudo conectar")
    return clientID

clientID = connect(19999)

retCode,sensorHandle=sim.simxGetObjectHandle(clientID,'Vision_sensor',sim.simx_opmode_blocking)

retCode, resolution, imaged=sim.simxGetVisionSensorDepthBuffer(clientID, sensorHandle,sim.simx_opmode_oneshot_wait)
retCode, resolution, image=sim.simxGetVisionSensorImage(clientID,sensorHandle,0,sim.simx_opmode_oneshot_wait)

img = np.array(image, dtype=np.uint8)
img.resize([resolution[1],resolution[0],3])
img=np.flipud(img)

imgd= np.array(imaged)
imgd.resize([resolution[1],resolution[0]])
imgd=np.flipud(imgd)
imgdaux=imgd.flatten()


u_res=resolution[1]
v_res=resolution[0]
near_clip=0.01
far_clip=3.5
xyzv=np.zeros((u_res*v_res,3))
rgbv=np.zeros((u_res*v_res,3))
focal_length = (640.0/2.0) / math.tan((83.0/2.0) * np.pi/ 180)
for u in range(u_res):
    for v in range(v_res):
            w = int(v_res * u + v)
            z = far_clip * imgdaux[w] + near_clip;
            y = (u - u_res / 2.0) * z / focal_length;
            x = (v - v_res / 2.0) * z / focal_length;
            xyzv[w][:]=np.array([x,y,z])
            rgbv[w][:]=img[u][v]
pcl = o3d.geometry.PointCloud()
pcl.points = o3d.utility.Vector3dVector(xyzv)
pcl.colors  = o3d.utility.Vector3dVector(rgbv/ 255.0)
o3d.visualization.draw_geometries([pcl])
