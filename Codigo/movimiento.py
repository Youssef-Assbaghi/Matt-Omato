# -*- coding: utf-8 -*-
"""
Created on Sun May  2 13:30:06 2021

@author: Youssef
"""
import math
import numpy as np
class Movimiento:
    def __init__(self,brazo,antebrazo,altura,muñequilla):
        self.b=brazo
        self.ab=antebrazo
        self.H=altura
        self.m=muñequilla
    
    def coordenadas(self,x,y,z):

        Axis5=180
        cabRAD=self.cabGrados*np.pi/180
        Axis1=math.atan2(y, x)
        M=math.sqrt(pow(x,2)+pow(y,2))
        xprima=M
        yprima=z

        Afx=math.cos(cabRAD)*self.m
        B=xprima-Afx
        Afy=math.sin(cabRAD)*self.m
        A=yprima+Afy-self.H;
        Hip=math.sqrt(pow(A,2)+pow(B,2))
        alfa=math.atan2(A,B)
        beta=math.acos((pow(self.b,2)-pow(self.ab,2)+pow(Hip,2))/(2*self.b*Hip))
        Axis2=alfa+beta
        gamma=math.acos((pow(self.b,2)+pow(self.ab,2)-pow(Hip,2))/(2*self.b*self.ab))
        Axis3=gamma
        Axis4=2*np.pi-cabRAD-Axis2-Axis3
        
        j0=90+Axis1*180/np.pi #joint0
        j1=90-Axis2*180/np.pi #joint1
        j2=180-Axis3*180/np.pi #joint2
        j3=180-Axis4*180/np.pi #joint3
        j4=Axis5 #joint5  Se ha dado en grados inicialmente
        print(j0,j1,j2,j3,j4)
        
        return j0*np.pi/180,j1*np.pi/180,j2*np.pi/180,j3*np.pi/180,j4*np.pi/180
        
        
        
        
        
        
        
        