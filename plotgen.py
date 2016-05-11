# -*- coding: utf-8 -*-
"""
Created on Tue May 10 17:13:31 2016

@author: Nikolaus Luhrs
"""
import matplotlib.pyplot as plt
import os
import numpy as np
import re
ferrites={'NiZnCu':{},'NiZnMn':{},'CO2Z':{}}
for f in ferrites.keys():
  ferrites[f]['GAIN_3d']='\\'+f+'\\GAIN_3D_'+f+'.csv'
  ferrites[f]['S11']='\\'+f+'\\S11_'+f+'.csv'
  ferrites[f]['RAD_EFF']='\\'+f+'\\RAD_EFF_'+f+'.csv'
def getheader(filename):#grabs the header
  fp=open(os.getcwd()+filename,'r')
  header=fp.readline()
  fp.close()
  return header.split(',')
def getsets(colheader):
  setstr=colheader.split(' - ')[1]
  fpz=re.search('ferrite_pos_z=\'[^\']*\'',setstr).group()[15:-1]
  Phi=re.search('Phi=\'[^\']*\'',setstr).group()[5:-4]
  Theta=re.search('Theta=\'[^\']*\'',setstr).group()[7:-4]
  Wb=re.search('Wb=\'[^\']*\'',setstr).group()[4:-1]  
  print Phi
  print Theta
  print Wb
  return()
if __name__=='__main__':
  header=getheader(ferrites['CO2Z']['GAIN_3d'])
  getsets(header[100])