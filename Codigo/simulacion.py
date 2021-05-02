# -*- coding: utf-8 -*-
"""
Created on Sun May  2 13:52:27 2021

@author: Youssef
"""
import robot
import movimiento
import numpy as np
import time
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
    
    
    
    
    
    
if __name__ == '__main__':
    print("Se crea el robot")
    robot = robot.Robot()
    robot.connect(19999)
    
    #Set Dummy
    returnCode,handle=robot.getObjectHandler('Dummy')
    dummy=handle
    returnCode,pos=robot.getObjectPosition(dummy)
    
    #SetJoints
    ret,Joint_Base=robot.getObjectHandler('Joint_Base0')
    ret,Joint_Hombro=robot.getObjectHandler('Joint_Hombro0')
    ret,Joint_Codo=robot.getObjectHandler('Joint_Codo0')
    ret,Joint_Muneca=robot.getObjectHandler('Joint_Muneca0')
    ret,Joint_Pinza=robot.getObjectHandler('Joint_Pinza')
    ret,Joint_Cam=robot.getObjectHandler('Joint_Cam0')
    
    print(Joint_Base, Joint_Hombro, Joint_Codo,Joint_Muneca,Joint_Cam,Joint_Pinza)
    
    static_simulation(Joint_Base, Joint_Hombro, Joint_Codo, Joint_Muneca, Joint_Cam, Joint_Pinza,robot)
    robot.getObjectPosition(dummy)
    
    

    