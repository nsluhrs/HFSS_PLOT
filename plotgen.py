# -*- coding: utf-8 -*-
"""
Created on Tue May 10 17:13:31 2016

@author: Nikolaus Luhrs
"""
import matplotlib.pyplot as plt
import os
import numpy as np
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
    for n in range(c[0],c[0]+len(data[c[0]:c[1]])):
      datalabels.append(getparam(header[n]))
    print len(data[c[0]:c[1]])
    labeled[casenames[ cs.index(c)]]=[data[c[0]:c[1]],datalabels]
    
  return labeled
def getFreqs(datafile):
  return np.genfromtxt(os.getcwd()+datafile,skip_header=1,delimiter=',').T[0]
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
      caseset.append((hs[n],None))
    else:
      caseset.append((hs[n],hs[n+1]))
  return (caseset,list(physstrs))
def getTPatFreq(dataset,freqindex):

  return dataset.T[freqindex].reshape((37,-1)).T

if __name__=='__main__':
  
  header=getheader(ferrites['CO2Z']['GAIN_3d'])
  labeled=getLabeled(ferrites['CO2Z']['GAIN_3d'])
  f=getFreqs(ferrites['CO2Z']['GAIN_3d'])
  for l in labeled.keys():
    c1=labeled[l]
    for n in range(21)+[]:
      plt.close('all')
      r=getTPatFreq(c1[0],n)
      r=r-np.min(r)
      #r=np.array([[1]*37]*73)
      t=np.linspace(0,np.pi,37) 
      p=np.linspace(0,2*np.pi,73)
      T,P=np.meshgrid(t,p)
      X,Y,Z=r*np.outer(np.sin(p),np.cos(t)),r*np.outer(np.sin(p),np.sin(t)),r*np.cos(P)
    
      from mpl_toolkits.mplot3d import Axes3D

      from matplotlib import cm
      
      step = 0.04
      maxval = 1.0
      ed=np.ones((r.shape[0]-1,r.shape[1]-1))
      for i in range(r.shape[0]-1):
        for j in range(r.shape[1]-1):
          ed[i][j]=(r[i][j]+r[i+1][j]+r[i][j+1]+r[i+1][j+1])/(4.*np.max(r))
      fig = plt.figure()
      ax = fig.add_subplot(111, projection='3d')
      ax.set_title(str(f[n]))
      
      ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=cm.jet(ed),shade=False)
      ax.set
      ax.set_xlabel(r'$\phi_\mathrm{real}$')
      ax.set_ylabel(r'$\phi_\mathrm{im}$')
      ax.set_zlabel(r'$V(\phi)$')
      sname=l.replace(':','=').replace(',','')
      plt.savefig('%.4d'%f[n]+('%.2f'%(f[n]-np.floor(f[n])))[1:]+sname+'.png',transparent=True)
      print '%.4d'%f[n]+('%.1f'%(f[n]-np.floor(f[n])))[1:]+sname+'.png'