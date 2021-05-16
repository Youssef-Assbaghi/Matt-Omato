# -*- coding: utf-8 -*-
"""
Created on Sun May  2 13:52:27 2021

@author: Youssef
"""
import robot
import movimiento
import pointcloud
import numpy as np
import time
import sim
def static_simulation(Joint_Base, Joint_Hombro, Joint_Codo,Joint_Muneca,Joint_Cam,Joint_Pinza,robot):
    print("static simulation")
    q0 = 120 * np.pi/180
    robot.setTargetPosition(Joint_Base,q0)
    time.sleep(3)
    q1 = -50 * np.pi/180
    robot.setTargetPosition(Joint_Hombro,q1)
    time.sleep(3)
    q2 = 120 * np.pi/180
    robot.setTargetPosition(Joint_Codo,q2)
    time.sleep(3)
    q3 = -120 * np.pi/180
    robot.setTargetPosition(Joint_Muneca,q3)
    time.sleep(3)
    q4 = -120 * np.pi/180
    robot.setTargetPosition(Joint_Pinza,q4)
    time.sleep(3)
    q5 = -20 * np.pi/180
    robot.setTargetPosition(Joint_Cam,q5)
    
    
def inf(i=0, step=1):
    #un generador de iteradores infinitos, como el xrange, pero infinito
    while True:
        yield i
        i+=step    
    
    
    
if __name__ == '__main__':
    q=[]
    print("Se crea el robot")
    robot = robot.Robot()
    robot.connect(19999)
    
    #Set Dummy
    returnCode,handle=robot.getObjectHandler('Dummy')
    dummy=handle
    returnCode,pos_d=robot.getObjectPosition(dummy)

    #SetJoints
    ret,Joint_Base=robot.getObjectHandler('Joint_Base0')
    ret,Joint_Hombro=robot.getObjectHandler('Joint_Hombro0')
    ret,Joint_Codo=robot.getObjectHandler('Joint_Codo0')
    ret,Joint_Muneca=robot.getObjectHandler('Joint_Muneca0')
    ret,Joint_Pinza=robot.getObjectHandler('Joint_Pinza')
    ret,Joint_Cam=robot.getObjectHandler('Joint_Cam0')
    ret,Joint_Movimiento_Pinza=robot.getObjectHandler('Barrett_openCloseJoint')
    ret,Joint_Movimiento_Pinza1=robot.getObjectHandler('Barrett_openCloseJoint0')
    ret,P_SD=robot.getObjectHandler('P_SD')
    ret,P_ST=robot.getObjectHandler('P_ST')
    ret,Joint_DD0=robot.getObjectHandler('Joint_DD0')
    ret,Joint_DI0=robot.getObjectHandler('Joint_DI0')
    ret,Joint_TD0=robot.getObjectHandler('Joint_TD0')
    ret,Joint_TI0=robot.getObjectHandler('Joint_TI0')



    ret,sensorHandle = robot.getObjectHandler('Vision_sensor0')
    print(Joint_Base, Joint_Hombro, Joint_Codo,Joint_Muneca,Joint_Cam,Joint_Pinza, sensorHandle)
    
    mov=movimiento.Movimiento(robot.brazo,robot.antebrazo,robot.altura,robot.muñeca)

    angulo=25

    vision_open3d=False
    centers = pointcloud.Get_Image(sensorHandle,robot, angulo, vision_open3d)
    print(centers)
    """
    #POS HOME:
    robot.setTargetPosition(Joint_Base,0)
    time.sleep(2)
    robot.setTargetPosition(Joint_Hombro,0)
    time.sleep(2)
    robot.setTargetPosition(Joint_Codo,0 )
    time.sleep(2)
    robot.setTargetPosition(Joint_Muneca,0)
    time.sleep(2)
    robot.setTargetPosition(Joint_Pinza,0)
    time.sleep(5)
    """
    #Aqui caluclamos la posicion del Dummy objetivo

    #ret,dummy_cubo=robot.getObjectHandler('Dummy_Cubo')
    #ret,pos=robot.getObjectPosition(dummy_cubo)
    #print(pos)
    
    ret, sphere = robot.getObjectHandler('Sphere0')
    """
    for ce in centers:
        pos=ce
        pos_correcion=[0.48,0.15,-0.2]
        posf=pos+pos_correcion
        q=mov.coordenadas(posf[0],posf[1],posf[2])
        robot.setTargetPosition(Joint_Base,q[0])
        time.sleep(2)
        robot.setTargetPosition(Joint_Codo, q[2])
        time.sleep(2)
        robot.setTargetPosition(Joint_Muneca, q[3])
        time.sleep(2)
        robot.setTargetPosition(Joint_Hombro,q[1])
        time.sleep(2)
        robot.actuarPinza(Joint_Movimiento_Pinza,Joint_Movimiento_Pinza1)
        time.sleep(2)
        res, Robotiq = sim.simxGetObjectHandle(robot.clientID, 'FC', sim.simx_opmode_blocking)
        returncode = sim.simxSetObjectParent(robot.clientID, sphere, Robotiq, True, sim.simx_opmode_blocking);
        robot.setTargetPosition(Joint_Pinza,q[4])
        time.sleep(2)
        sim.simxSetObjectIntParameter(robot.clientID, sphere, sim.sim_shapeintparam_static, 0, sim.simx_opmode_oneshot)
        pos = [-0.9, 0.0126, 0.55]
        posf = pos
        q = mov.coordenadas(posf[0], posf[1], posf[2])
        robot.setTargetPosition(Joint_Hombro, q[1])
        time.sleep(2)
        robot.setTargetPosition(Joint_Base, q[0])
        time.sleep(2)
        robot.setTargetPosition(Joint_Codo, q[2])
        time.sleep(2)
        robot.setTargetPosition(Joint_Muneca, q[3])
        time.sleep(2)
        robot.setTargetPosition(Joint_Pinza, q[4])
        time.sleep(2)
        robot.actuarPinza(Joint_Movimiento_Pinza, Joint_Movimiento_Pinza1)
        time.sleep(2)
        returncode=sim.simxSetObjectParent(robot.clientID, sphere,0, False, sim.simx_opmode_blocking)
        #sim.simxSetObjectIntParameter(robot.clientID, sphere, sim.sim_shapeintparam_static, 1, sim.simx_opmode_oneshot)
        time.sleep(2)
        returncode=sim.simxSetObjectParent(robot.clientID, sphere,1, False, sim.simx_opmode_blocking)
        
        
    """
        
    for i in inf():
        centers = pointcloud.Get_Image(sensorHandle,robot, angulo, vision_open3d)
        if len(centers)==0:#No se detecta tomate
            robot.move(100,Joint_DD0,Joint_DI0,Joint_TD0,Joint_TI0,1)
            time.sleep(1)
            robot.move(0,Joint_DD0,Joint_DI0,Joint_TD0,Joint_TI0,0)
        else:
            for ce in centers:
                pos=ce
                pos_correcion=[0.48,0.15,-0.2]
                posf=pos+pos_correcion
                q=mov.coordenadas(posf[0],posf[1],posf[2])
                robot.setTargetPosition(Joint_Base,q[0])
                time.sleep(2)
                robot.setTargetPosition(Joint_Codo, q[2])
                time.sleep(2)
                robot.setTargetPosition(Joint_Muneca, q[3])
                time.sleep(2)
                robot.setTargetPosition(Joint_Hombro,q[1])
                time.sleep(2)
                robot.actuarPinza(Joint_Movimiento_Pinza,Joint_Movimiento_Pinza1)
                time.sleep(2)
                res, Robotiq = sim.simxGetObjectHandle(robot.clientID, 'FC', sim.simx_opmode_blocking)
                returncode = sim.simxSetObjectParent(robot.clientID, sphere, Robotiq, True, sim.simx_opmode_blocking);
                robot.setTargetPosition(Joint_Pinza,q[4])
                time.sleep(2)
                sim.simxSetObjectIntParameter(robot.clientID, sphere, sim.sim_shapeintparam_static, 0, sim.simx_opmode_oneshot)
                pos = [-0.9, 0.0126, 0.55]
                posf = pos
                q = mov.coordenadas(posf[0], posf[1], posf[2])
                robot.setTargetPosition(Joint_Hombro, q[1])
                time.sleep(2)
                robot.setTargetPosition(Joint_Base, q[0])
                time.sleep(2)
                robot.setTargetPosition(Joint_Codo, q[2])
                time.sleep(2)
                robot.setTargetPosition(Joint_Muneca, q[3])
                time.sleep(2)
                robot.setTargetPosition(Joint_Pinza, q[4])
                time.sleep(2)
                robot.actuarPinza(Joint_Movimiento_Pinza, Joint_Movimiento_Pinza1)
                time.sleep(2)
                returncode=sim.simxSetObjectParent(robot.clientID, sphere,0, False, sim.simx_opmode_blocking)
                #sim.simxSetObjectIntParameter(robot.clientID, sphere, sim.sim_shapeintparam_static, 1, sim.simx_opmode_oneshot)
                time.sleep(2)
                returncode=sim.simxSetObjectParent(robot.clientID, sphere,1, False, sim.simx_opmode_blocking)
                                




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    