# -*- coding: utf-8 -*-
"""
Created on Tue May 10 17:13:31 2016

@author: Nikolaus Luhrs
"""
import matplotlib.pyplot as plt
import os
import numpy as np
import re
ferrites={'NIZNCU':{},'NIZNMN':{},'CO2Z':{}}
for f in ferrites.keys():
  
  ferrites[f]['GAIN_3d']='\\'+f+'\\GAIN_3D_'+f+'.csv'
  ferrites[f]['S11']='\\'+f+'\\S11_'+f+'.csv'
  ferrites[f]['RAD_EFF']='\\'+f+'\\RAD_EFF_'+f+'.csv'
def getheader(filename):#grabs the header
  fp=open(os.getcwd()+filename,'r')
  header=fp.readline()
  fp.close()
  return header.split(',')
def getparam(colheader):
  if colheader=='"Freq [MHz]"':
    return {'xunits':'MHz'}
  params=[]
  for p in colheader.split(' '):
    if '=' in p:
      params.append(p)
  paramValue={}
  for p in params:
    paramValue[p.split('=')[0]]=p.split("'")[1]
  return paramValue
def getUnlabeled(datafile):
  return np.genfromtxt(os.getcwd()+datafile,skip_header=1,delimiter=',')
def getLabeled(datafile):
  header=getheader(datafile)
  data=getUnlabeled(datafile).T
  cs,casenames=getcases(header)
  print cs
  labeled={}
  for c in cs:
    print casenames[ cs.index(c)]
    datalabels=[]
    for n in range(c[0],c[1]+1):
      datalabels.append(getparam(header[n]))
    labeled[casenames[ cs.index(c)]]=[data[c[0]:c[1]],datalabels]
  return labeled
def getcases(header):
  physkeys=['ferrite_pos_z','Wb']
  phys=[]
  hs=[]
  physstrs=[]
  for h in header[1:]:
    ap=getparam(h)
    compstr=''
    for p in physkeys:
      compstr=compstr+p+':'+ap[p]+', '
    phys.append(compstr[:-2])  
  for uc in set(phys):
    hs.append(phys.index(uc)+1)
    physstrs.append(uc)
  #print set(phys)
  caseset=[]  
  hs.sort()
  for n in range(len(hs)):
    if n == len(hs)-1:
      caseset.append((hs[n],len(header)-1))
    else:
      caseset.append((hs[n],hs[n+1]-1))
  return (caseset,list(physstrs))
  
if __name__=='__main__':
  header=getheader(ferrites['CO2Z']['GAIN_3d'])
  labeled=getLabeled(ferrites['CO2Z']['GAIN_3d'])
  