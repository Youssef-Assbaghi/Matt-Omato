 # -*- coding: utf-8 -*-
"""
Created on Sun May  2 11:40:37 2021

@author: Youssef
"""

import sim
import math


class Robot:
    def __init__(self):
        self.clientID=0
        
    def getClientID(self):
        return self.clientID
    def connect(self,port):
    # Establece la conexión a COPPELIA
    # El port debe coincidir con el puerto de conexión en VREP  -- DALE AL PLAY !!!
    # retorna el número de cliente o -1 si no puede establecer conexión
        sim.simxFinish(-1) # just in case, close all opened connections
        clientID=sim.simxStart('127.0.0.1',port,True,True,2000,5) # Conectarse
        if clientID == 0: print("conectado a", port)
        else: print("no se pudo conectar")
        self.clientID = clientID
        return self.clientID
    
    def getObjectHandler(self,part):
        returnCode,handle=sim.simxGetObjectHandle(self.clientID,part,sim.simx_opmode_blocking)
        return returnCode,handle

    def getObjectPosition(self,part):
        returnCode,pos=sim.simxGetObjectPosition(self.clientID, part, -1, sim.simx_opmode_blocking)
        print("Dummy:",returnCode," ",pos)
        return returnCode,pos
    
    def getJointPosition(self,part):
        returnCode, joint = sim.simxGetJointPosition(self.clientID, part, sim.simx_opmode_blocking)
        return returnCode,joint
        
    def setTargetPosition(self,part,angle):
        returnCode = sim.simxSetJointTargetPosition(self.clientID, part, angle, sim.simx_opmode_oneshot)
        return returnCode
    
    def setTargetVel(self,v1,h):
        for i in h:
            sim.simxSetJointTargetVelocity(self.clientID, i[1], v1, sim.simx_opmode_oneshot)
        
    def move(self,vel,obj1,obj2,obj3,obj4,direction):
        #Direction puede ser 0 Stop, 1 Alante, 2 Atras
        h=[0,0,0,0]
        h[0]=self.getObjectHandler(self.clientID,obj1,sim.simx_opmode_blocking)
        h[1]=self.getObjectHandler(self.clientID,obj2,sim.simx_opmode_blocking)
        h[2]=self.getObjectHandler(self.clientID,obj3,sim.simx_opmode_blocking)
        h[3]=self.getObjectHandler(self.clientID,obj4,sim.simx_opmode_blocking)
        if direction==0:
            v1=0
        elif direction==1:   
            v1=vel*math.pi/180
        else:
            v1=vel*math.pi/180
            v1=-v1   
        self.setTargetVel(v1,h)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        