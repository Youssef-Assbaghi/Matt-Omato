# -*- coding: utf-8 -*-
"""
Created on Sun May  2 13:52:27 2021

@author: Youssef and Marti
"""
import robot
import movimiento
import numpy as np
import time
import sim
def static_simulation(Joint_Base, Joint_Hombro, Joint_Codo,Joint_Muneca,Joint_Cam,Joint_Pinza,robot):
    print("static simulation")
    q0 = 120 * np.pi/180
    robot.setTargetPosition(Joint_Base,0)
    time.sleep(3)
    q1 = -50 * np.pi/180
    robot.setTargetPosition(Joint_Hombro,0)
    time.sleep(3)
    q2 = 120 * np.pi/180
    robot.setTargetPosition(Joint_Codo,0)
    time.sleep(3)
    q3 = -120 * np.pi/180
    robot.setTargetPosition(Joint_Muneca,0)
    time.sleep(3)
    q4 = -120 * np.pi/180
    robot.setTargetPosition(Joint_Pinza,0)
    time.sleep(3)
    q5 = -20 * np.pi/180
    robot.setTargetPosition(Joint_Cam,q5)
    
    
    
    
    
    
if __name__ == '__main__':
    print("Se crea el robot")
    robot = robot.Robot()
    robot.connect(19999)
    #robot.getSize()
    mov=movimiento.Movimiento(robot.brazo,robot.antebrazo,robot.altura,robot.muñeca)
    #mov=movimiento.Movimiento(579,713.9,486,150)
    #mov=movimiento.Movimiento(185,138,172,85)
    #Set Dummy
    returnCode,handle=robot.getObjectHandler('Dummy')
    dummy=handle
    returnCode,pos_d=robot.getObjectPosition(dummy)
    
    #SetJoints
    ret,Joint_Base=robot.getObjectHandler('Joint_Base1')
    ret,Joint_Hombro=robot.getObjectHandler('Joint_Hombro1')
    ret,Joint_Codo=robot.getObjectHandler('Joint_Codo1')
    ret,Joint_Muneca=robot.getObjectHandler('Joint_Muneca1')
    ret,Joint_Pinza=robot.getObjectHandler('Joint_Pinza')
    ret,Joint_Cam=robot.getObjectHandler('Joint_Cam0')
    
    print(Joint_Base, Joint_Hombro, Joint_Codo,Joint_Muneca,Joint_Cam,Joint_Pinza)
   
    
    
    #static_simulation(Joint_Base, Joint_Hombro, Joint_Codo, Joint_Muneca, Joint_Cam, Joint_Pinza,robot)
    q=[]
    #q=mov.coordenadas(-1.7378114640712736,-3.47056850194931,-0.03983629047870636)
   
    """
    Con estos valores se acerca a la pieza que hemos puesto
    Lo que significa que se acerca a la posicion (-1.08,2.08,0.17)  
    del Coppelia
    
    POS HOME:
    """
    
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
    Aqui caluclamos la posicion del Dummy objetivo
    """
    ret,dummy_cubo=robot.getObjectHandler('Dummy_Cubo')
    ret,pos=robot.getObjectPosition(dummy_cubo)
    print(pos)
    
    q=mov.coordenadas(pos[0]-pos_d[0],pos[1]-pos_d[1],pos[2])
    
    #q=mov.coordenadas(0,0,1.5)
    robot.setTargetPosition(Joint_Base,q[0])
    time.sleep(2)
    robot.setTargetPosition(Joint_Hombro,q[1])
    time.sleep(2)
    robot.setTargetPosition(Joint_Codo,q[2] )
    time.sleep(2)
    robot.setTargetPosition(Joint_Muneca,q[3])
    time.sleep(2)
    robot.setTargetPosition(Joint_Pinza,q[4])
    robot.getObjectPosition(dummy)
    
    
    """
    
    
     (0,0,0)=[-1.0789602994918823, 1.8167195320129395, 0.9268665313720703]
        (1,1,1)=[-1.6165688037872314, 1.7138609886169434, 0.7967258095741272]
        [-1.075,2.025,0.05]=regla de 3
    """

    

    