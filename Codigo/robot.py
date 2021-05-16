 # -*- coding: utf-8 -*-
"""
Created on Sun May  2 11:40:37 2021

@author: Youssef
"""

import sim
import math
import time

class Robot:
    def __init__(self):
        self.clientID=0
        self.altura=0.5628
        self.brazo=0.4268
        self.antebrazo=0.6219
        self.muñeca=0.1665
        self.cabGrados=0
        self.pinza=True
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

    def get_proximitysensor(self,psensor):
        errorCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector=sim.simxReadProximitySensor(self.clientID, psensor, sim.simx_opmode_blocking)
        return [detectionState]

    def actuarPinza(self,Joint_Movimiento_Pinza,Joint_Movimiento_Pinza1):

        """
        Le pasamos los hagndlers de Joints que controlan los tres dedos de la pinza
        Es importante deshabilitar la interfaz grafica del robot para poder hacer que la pinza funcione
        Debe tener un sleep de 6 segundos ya que se cierra poco a poco
        """

        if self.pinza:   
            sim.simxSetJointTargetVelocity(self.clientID, Joint_Movimiento_Pinza, -0.2, sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(self.clientID, Joint_Movimiento_Pinza1, -0.2, sim.simx_opmode_oneshot)
            time.sleep(1)
            self.pinza=False

        else:
            sim.simxSetJointTargetVelocity(self.clientID, Joint_Movimiento_Pinza,0.02, sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(self.clientID, Joint_Movimiento_Pinza1, 0.02, sim.simx_opmode_oneshot)
            self.pinza=True
            time.sleep(1)
            

    
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
    
    def getSize(self):
        ret,Base=self.getObjectHandler('Base0')
        ret,Brazo=self.getObjectHandler('Brazo_3')
        ret,Antebrazo=self.getObjectHandler('Brazo_4')
        ret,Muñequilla=self.getObjectHandler('Muneca0')
        
        error,zmax_b=sim.simxGetObjectFloatParameter(self.clientID,Base,20,sim.simx_opmode_blocking)
        error,zmin_b=sim.simxGetObjectFloatParameter(self.clientID,Base,17,sim.simx_opmode_blocking)
        
        self.base=(zmax_b-zmin_b)*1000*2
        
        error,xmax_bz=sim.simxGetObjectFloatParameter(self.clientID,Brazo,24,sim.simx_opmode_blocking)
        error,xmin_bz=sim.simxGetObjectFloatParameter(self.clientID,Brazo,21,sim.simx_opmode_blocking)
        
        self.brazo=(xmax_bz-xmin_bz)*1000
        
        error,xmax_ab=sim.simxGetObjectFloatParameter(self.clientID,Antebrazo,24,sim.simx_opmode_blocking)
        error,xmin_ab=sim.simxGetObjectFloatParameter(self.clientID,Antebrazo,21,sim.simx_opmode_blocking)
        
        self.antebrazo=(xmax_ab-xmin_ab)*1000
        
        error,xmax_m=sim.simxGetObjectFloatParameter(self.clientID,Muñequilla,24,sim.simx_opmode_blocking)
        error,xmin_m=sim.simxGetObjectFloatParameter(self.clientID,Muñequilla,21,sim.simx_opmode_blocking)
        
        self.muñeca=(xmax_m-xmin_m)*1000
       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        