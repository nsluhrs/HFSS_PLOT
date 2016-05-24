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
def getLabeled(datafile,physkeys=['ferrite_pos_z','Wb']):
  header=getheader(datafile)
  data=getUnlabeled(datafile).T
  cs,casenames=getcases(header)
  #print cs
  labeled={}
  for c in cs:
    #print casenames[ cs.index(c)]
    datalabels=[]
    for n in range(c[0],c[0]+len(data[c[0]:c[1]])):
      datalabels.append(getparam(header[n]))
    #print len(data[c[0]:c[1]])
    labeled[casenames[ cs.index(c)]]=[data[c[0]:c[1]],datalabels]
    
  return labeled
def getFreqs(datafile):
  return np.genfromtxt(os.getcwd()+datafile,skip_header=1,delimiter=',').T[0]
def getcases(header,physkeys=['ferrite_pos_z','Wb']):
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
def thermalLoss(ferrite):
  s11=getUnlabeled(ferrites[ferrite]['S11']).T[1:]
  radeff=getUnlabeled(ferrites[ferrite]['RAD_EFF']).T[1:]
  
  mags1s=1-10**(s11/20.)
  return (1-radeff.T)*mags1s.T
def getslice(data,plane):
  if len(plane)!=2:raise ValueError('plane must be of form XY,YZ,XZ \n order does not matter')
  uv=[]
  for a in ['X','Y','Z']:uv+=[a in plane]
  X,Y,Z=uv
  inds=[]
  if X and Y:
    for n in xrange(len(data[1])):
      d=data[1][n]
      if d['Theta']=='90deg':
        inds.append(n)
    return inds
  if X and Z:
    for n in xrange(len(data[1])):
      d=data[1][n]
      if d['Phi']=='0deg' or d['Phi']=='180deg':
        inds.append(n)
    inds=inds[::2]+inds[-3::-2]
    return inds
  if Y and Z:
    for n in xrange(len(data[1])):
      d=data[1][n]
      if d['Phi']=='90deg' or d['Phi']=='270deg':
        inds.append(n)
    inds=inds[::2]+inds[-3::-2]
    return inds
  
if __name__=='__main__':
  
  header=getheader(ferrites['NIZNMN']['GAIN_3d'])
  labeled=getLabeled(ferrites['NIZNMN']['GAIN_3d'])
  f=getFreqs(ferrites[fer]['GAIN_3d'])
  for fer in ferrites.keys():
    labeled=getLabeled(ferrites[fer]['GAIN_3d'])
    for k in labeled.keys():
      print k
  labels=['XY','YZ','XZ']
  datasets=[]
  from matplotlib import cm

  for label in labels:
    datasets.append(np.array(labeled[k][0])[getslice(labeled[k],plane=label)])
  plt.close('all')
  pts=np.linspace(0,2*np.pi,73)
  for n in range(15,21):plt.polar(pts,10**(datasets[0].T[n]/20),label=str(round(f[n],2))+' XY',color=cm.jet((n-15.)/5.))
  for n in range(15,21):plt.polar(pts-np.pi/2,10**(datasets[2].T[n]/20),label=str(round(f[n],2))+' XZ',color=cm.jet((n-15.)/5.))
  plt.legend(loc=0)  

  
  
  
      
  '''
  for fer in ferrites.keys():
    plt.close('all')
    f=getFreqs(ferrites[fer]['GAIN_3d'])
    name=getheader(ferrites[fer]['RAD_EFF'])[1:]
    name=['  - total length  400 mm 1 mm of ferrrite on bottom only','  - total length 1000 mm 1 mm of ferrrite on bottom only','  - total length  400 mm 1 mm of ferrrite both sides','  - total length 1000 mm 1 mm of ferrrite on both sides']
    for q in range(len(thermalLoss(fer).T)):
      plt.plot(f,100*thermalLoss(fer).T[q],label=name[q].split(' - ')[1])
      np.savetxt(fer+name[q].split(' - ')[1]+'_heat_loss.csv',thermalLoss(fer).T[q],delimiter=',')
    plt.legend(loc=0)
    plt.ylim(0,100)
    plt.xlim(3,300)
    plt.title(fer+'\n'+'Power to Heat')
    s11=getUnlabeled(ferrites['NIZNMN']['S11']).T[1:]
    radeff=getUnlabeled(ferrites[fer]['RAD_EFF']).T[1:]
    plt.ylabel('% power to heat')
    mng = plt.get_current_fig_manager()
       
    plt.show()
    mng.window.showFullScreen()
    plt.savefig(fer+'heat'+'.png')
    plt.close('all')
    for q in range(len(thermalLoss(fer).T)):
      mags1s=1-10**(s11[q]/20.)
      
      plt.plot(f,mags1s*100,label=name[q].split(' - ')[1])
    plt.legend(loc=0)
    
    plt.ylabel('% power to antenna')
    plt.title(fer+'\n'+'$S_{1,freespace}$')
    mng = plt.get_current_fig_manager()
    plt.ylim(0,100)
    plt.xlim(3,300)
    plt.show()
    mng.window.showFullScreen()
    plt.savefig(fer+'s11'+'.png')
    plt.close('all')
    for q in range(len(thermalLoss(fer).T)):
      mags1s=1-10**(s11[q]/20.)
      magpow=mags1s*radeff[q]
      plt.plot(f,magpow*100,label=name[q].split(' - ')[1])
      np.savetxt(fer+name[q].split(' - ')[1]+'_radiated.csv',magpow,delimiter=',')
    mng = plt.get_current_fig_manager()
    plt.ylabel('% power radiated')
    plt.ylim(0,100)
    plt.xlim(3,300)
    plt.title(fer+'\n'+'Radiated')
    plt.legend(loc=0)
    plt.show()
    mng.window.showFullScreen()
    plt.savefig(fer+'rad'+'.png')
  plt.close('all')
  '''
  for l in labeled.keys():
    c1=labeled[l]
    
    
  ''' 
    for n in range(21)+[]:
      plt.close('all')
      r=10**(getTPatFreq(c1[0],n)/20.)
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
      
      ax.set_xlabel(r'$\phi_\mathrm{real}$')
      ax.set_ylabel(r'$\phi_\mathrm{im}$')
      ax.set_zlabel(r'$V(\phi)$')
      sname=l.replace(':','=').replace(',','')
      plt.savefig('%.4d'%f[n]+('%.2f'%(f[n]-np.floor(f[n])))[1:]+sname+'.png',transparent=True)
      print '%.4d'%f[n]+('%.1f'%(f[n]-np.floor(f[n])))[1:]+sname+'.png'
  '''