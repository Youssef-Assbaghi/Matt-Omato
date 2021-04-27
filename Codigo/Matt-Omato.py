#!/usr/bin/env python
# coding: utf-8

# In[42]:


import sim
import numpy as np
import math
import time


# In[43]:


def connect(port):
# Establece la conexión a COPPELIA
# El port debe coincidir con el puerto de conexión en VREP  -- DALE AL PLAY !!!
# retorna el número de cliente o -1 si no puede establecer conexión
    sim.simxFinish(-1) # just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',port,True,True,2000,5) # Conectarse
    if clientID == 0: print("conectado a", port)
    else: print("no se pudo conectar")
    return clientID


# In[44]:


clientID = connect(19999)


# In[45]:


returnCode,handle=sim.simxGetObjectHandle(clientID,'Dummy',sim.simx_opmode_blocking)
dummy = handle
print(dummy)


# In[46]:


returnCode,pos=sim.simxGetObjectPosition(clientID, dummy, -1, sim.simx_opmode_blocking)
print(pos)


# In[47]:


ret,Joint_Base0=sim.simxGetObjectHandle(clientID,'Joint_Base0',sim.simx_opmode_blocking)
ret,Joint_Hombro0=sim.simxGetObjectHandle(clientID,'Joint_Hombro0',sim.simx_opmode_blocking)
ret,Joint_Codo0=sim.simxGetObjectHandle(clientID,'Joint_Codo0',sim.simx_opmode_blocking)
ret,Joint_Muneca0=sim.simxGetObjectHandle(clientID,'Joint_Muneca0',sim.simx_opmode_blocking)


# In[48]:


ret,Joint_Base=sim.simxGetObjectHandle(clientID,'Joint_Base',sim.simx_opmode_blocking)
ret,Joint_Hombro=sim.simxGetObjectHandle(clientID,'Joint_Hombro',sim.simx_opmode_blocking)
ret,Joint_Codo=sim.simxGetObjectHandle(clientID,'Joint_Codo',sim.simx_opmode_blocking)
ret,Joint_Muneca=sim.simxGetObjectHandle(clientID,'Joint_Muneca',sim.simx_opmode_blocking)
ret,Joint_Rotacion=sim.simxGetObjectHandle(clientID,'Joint_Rotacion',sim.simx_opmode_blocking)
ret,Joint_Cam=sim.simxGetObjectHandle(clientID,'Joint_Cam',sim.simx_opmode_blocking)
print(Joint_Base, Joint_Hombro, Joint_Codo,Joint_Muneca,Joint_Rotacion,Joint_Cam)


# In[49]:


returnCode, pos0 = sim.simxGetJointPosition(clientID, Joint_Base, sim.simx_opmode_blocking)
print(pos0)


# In[9]:


returnCode, pos1 = sim.simxGetJointPosition(clientID, Joint_Hombro, sim.simx_opmode_blocking)
print(pos1)


# In[10]:


returnCode, pos2 = sim.simxGetJointPosition(clientID, Joint_Codo, sim.simx_opmode_blocking)
print(pos2)


# In[11]:


returnCode, pos3 = sim.simxGetJointPosition(clientID, Joint_Muneca, sim.simx_opmode_blocking)
print(pos3)


# In[12]:


returnCode, pos4 = sim.simxGetJointPosition(clientID, Joint_Rotacion, sim.simx_opmode_blocking)
print(pos4)


# In[13]:


q0 = 0 * np.pi/180
returnCode = sim.simxSetJointTargetPosition(clientID, Joint_Base0, q0, sim.simx_opmode_oneshot)
print(returnCode)
time.sleep(3)

# In[14]:


q1 = -50 * np.pi/180
returnCode = sim.simxSetJointTargetPosition(clientID, Joint_Hombro0, q1, sim.simx_opmode_oneshot)
print(returnCode)
time.sleep(3)

# In[15]:


q2 = 120 * np.pi/180
returnCode = sim.simxSetJointTargetPosition(clientID, Joint_Codo0, q2, sim.simx_opmode_oneshot)
print(returnCode)
time.sleep(3)

# In[20]:


q3 = -120 * np.pi/180
returnCode = sim.simxSetJointTargetPosition(clientID, Joint_Muneca0, q3, sim.simx_opmode_oneshot)
print(returnCode)

time.sleep(3)
# In[21]:


q4 = -20 * np.pi/180
returnCode = sim.simxSetJointTargetPosition(clientID, Joint_Rotacion, q4, sim.simx_opmode_oneshot)
print(returnCode)

time.sleep(3)
# In[22]:


q5 = -20 * np.pi/180
returnCode = sim.simxSetJointTargetPosition(clientID, Joint_Cam, q5, sim.simx_opmode_oneshot)
print(returnCode)
time.sleep(3)

# In[23]:


returnCode,pos=sim.simxGetObjectPosition(clientID, dummy, -1, sim.simx_opmode_blocking)
print(pos)
time.sleep(3)

# ## Control ruedas
# 

# In[50]:


def Delante(vel):
    h=[0,0,0,0]
    h[0]=sim.simxGetObjectHandle(clientID,'Joint_DD0',sim.simx_opmode_blocking)
    h[1]=sim.simxGetObjectHandle(clientID,'Joint_DI0',sim.simx_opmode_blocking)
    h[2]=sim.simxGetObjectHandle(clientID,'Joint_TI0',sim.simx_opmode_blocking)
    h[3]=sim.simxGetObjectHandle(clientID,'Joint_TD0',sim.simx_opmode_blocking)
    v1=vel*math.pi/180
    
    sim.simxSetJointTargetVelocity(clientID, h[0][1], v1, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, h[1][1], v1, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, h[2][1], v1, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, h[3][1], v1, sim.simx_opmode_oneshot)


# In[51]:


def Atras(vel):
    h=[0,0,0,0]
    h[0]=sim.simxGetObjectHandle(clientID,'Joint_DD0',sim.simx_opmode_blocking)
    h[1]=sim.simxGetObjectHandle(clientID,'Joint_DI0',sim.simx_opmode_blocking)
    h[2]=sim.simxGetObjectHandle(clientID,'Joint_TI0',sim.simx_opmode_blocking)
    h[3]=sim.simxGetObjectHandle(clientID,'Joint_TD0',sim.simx_opmode_blocking)
    v1=vel*math.pi/180
    
    sim.simxSetJointTargetVelocity(clientID, h[0][1], -v1, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, h[1][1], -v1, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, h[2][1], -v1, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, h[3][1], -v1, sim.simx_opmode_oneshot)


# In[52]:


def Stop():
    h=[0,0,0,0]
    h[0]=sim.simxGetObjectHandle(clientID,'Joint_DD0',sim.simx_opmode_blocking)
    h[1]=sim.simxGetObjectHandle(clientID,'Joint_DI0',sim.simx_opmode_blocking)
    h[2]=sim.simxGetObjectHandle(clientID,'Joint_TI0',sim.simx_opmode_blocking)
    h[3]=sim.simxGetObjectHandle(clientID,'Joint_TD0',sim.simx_opmode_blocking)
    
    sim.simxSetJointTargetVelocity(clientID, h[0][1], 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, h[1][1], 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, h[2][1], 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, h[3][1], 0, sim.simx_opmode_oneshot)


# In[55]:


Delante(100)
time.sleep(3)

# In[54]:


Atras(100)

time.sleep(3)
# In[56]:


Stop()

time.sleep(3)
# In[129]:


# import numpy as np
# import sympy as sp
# from sympy import *
# from sympy.physics.vector import init_vprinting
# init_vprinting(use_latex='mathjax', pretty_print=False)


# # In[132]:


# from sympy.physics.mechanics import dynamicsymbols
# theta1, theta2,theta3, theta4,theta5, d3, l1, l2, l3,l4,l5, theta, alpha, a, d = dynamicsymbols('theta1 theta2 theta3 theta4 theta5 d3 l1 l2 l3 l4 l5 theta alpha a d')
# theta1, theta2,theta3, theta4,theta5, d3, lc,  l1, l2, l3,l4,l5, theta, alpha, a, d 


# In[ ]:




