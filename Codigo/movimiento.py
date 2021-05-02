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

        cabGrados=0
        Axis5=90 #Giro de la pinza
        Pinza=110
        cabRAD=cabGrados*np.pi/180
        
        Axis1=math.atan2(y, x)
        M=math.sqrt(pow(x,2)+pow(y, 2))
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
        Axis1Grados=Axis1*180/np.pi
        Axis2Grados=90-Axis2*180/np.pi
        Axis3Grados=180-Axis3*180/np.pi
        Axis4Grados=180-Axis4*180/np.pi
        
        return Axis1Grados,Axis2Grados,Axis3Grados,Axis4Grados,Axis5,Pinza
        
        
        
        
        
        
        