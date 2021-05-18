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

    
def inf(i=0, step=1):
    #un generador de iteradores infinitos, como el xrange, pero infinito
    while True:
        yield i
        i+=step    
      
    
    
    
if __name__ == '__main__':
    q=[]
    print("Se crea el robot")
    robot = robot.Robot()
    Joint_Base,Joint_Hombro,Joint_Codo,Joint_Muneca,Joint_Pinza,Joint_Cam,Joint_Movimiento_Pinza,Joint_Movimiento_Pinza1,P_SD,P_ST,FC,sensorHandle,dummy=robot.iniciar_robot()
    mov=movimiento.Movimiento(robot.brazo,robot.antebrazo,robot.altura,robot.muñeca)

    print(Joint_Base,Joint_Hombro,Joint_Codo,Joint_Muneca,Joint_Pinza,Joint_Cam,Joint_Movimiento_Pinza,Joint_Movimiento_Pinza1,P_SD,P_ST,FC,sensorHandle,dummy)
    
    angulo=50
    tomates=12
    vision_open3d=False
    """
    #POS HOME:
    robot.posHome(Joint_Base,Joint_Hombro,Joint_Codo,Joint_Muneca,Joint_Pinza)
    """
    #Aqui cogemos todos los Handles de los tomates
    toma=[]
    for i in range(tomates):
        ret, sphere = robot.getObjectHandler('Tomate'+str(i))
        auxv = [sphere]
        auxv.append(np.array(sim.simxGetObjectPosition(robot.clientID,sphere,-1,sim.simx_opmode_blocking)[1]))
        toma.append(auxv)
    direccion=1
    ultra_dir=P_SD
    aux_giro=0
    for i in inf():
        errorCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector=sim.simxReadProximitySensor(robot.clientID, ultra_dir, sim.simx_opmode_blocking)
        if detectionState:
            if direccion==2:
                break
            direccion=2
            ultra_dir=P_ST
            robot.setTargetPosition(Joint_Cam, np.pi/2)
            angulo=angulo+90
            time.sleep(1.5)
            aux_giro=-0.001
        else:
            centers = pointcloud.Get_Image(sensorHandle,robot, angulo, vision_open3d)
            if len(centers)==0:#No se detecta tomate
                robot.move(100,'Joint_DD0','Joint_DI0','Joint_TD0','Joint_TI0',direccion)
                time.sleep(1)
                robot.move(0,'Joint_DD0','Joint_DI0','Joint_TD0','Joint_TI0',0)
            else:#Se ha detectado un tomate, como minimo
                print(centers)
                for ce in centers:#En centers estan los tomates encontrados
                    pos=ce
                    pos_correcion=[0.5,0.0,0.0]
                    posf=pos+pos_correcion
                    q=mov.coordenadas(posf[0],posf[1],posf[2])#Cinematica inversa a posf
                    robot.setTargetPosition(Joint_Base,q[0])
                    time.sleep(2)
                    robot.setTargetPosition(Joint_Codo, q[2])
                    time.sleep(2)
                    robot.setTargetPosition(Joint_Hombro,q[1])
                    time.sleep(2)
                    robot.setTargetPosition(Joint_Muneca, q[3])
                    time.sleep(2)
                    bestdists=99999
                    point=-1
                    #Para conseguir la relación padre-hijo, necesitamos saber que tomate estamos cogiendo
                    ret, pos_d = robot.getObjectPosition(dummy)
                    for toa in toma:
                        auxdist=np.linalg.norm(np.array(pos_d) - toa[1])
                        if(auxdist<bestdists):
                            bestdists = auxdist
                            point = toa
                    pos_d-point[1]
                    returncode=sim.simxSetObjectParent(robot.clientID, point[0],FC, True, sim.simx_opmode_blocking)
                    robot.actuarPinza(Joint_Movimiento_Pinza,Joint_Movimiento_Pinza1)#Cerrar pinza
                    time.sleep(2)
                    robot.setTargetPosition(Joint_Pinza,q[4])
                    time.sleep(2)
                    pos_caja = [-0.8, 0.0+aux_giro, 0.71]#posicion de la caja
                    posf = pos_caja
                    q = mov.coordenadas(posf[0], posf[1], posf[2])#Cinematica inversa a posf
                    robot.ir_caja(Joint_Base,Joint_Hombro,Joint_Codo,Joint_Muneca,q)#Ir a la posicion de la caja
                   
                    #Deshacemos la relacion padre-hijo
                    returncode=sim.simxSetObjectParent(robot.clientID, point[0], -1, True, sim.simx_opmode_blocking)
                    robot.actuarPinza(Joint_Movimiento_Pinza, Joint_Movimiento_Pinza1)#Abrir pinza
                    time.sleep(0.5)
                    sim.simxSetObjectIntParameter(robot.clientID, point[0], sim.sim_shapeintparam_static, 0, sim.simx_opmode_oneshot)
                    time.sleep(1.5)
                    robot.setTargetPosition(Joint_Pinza, 0)
                    sim.simxSetObjectIntParameter(robot.clientID, point[0], sim.sim_shapeintparam_static, 1, sim.simx_opmode_oneshot)









    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    