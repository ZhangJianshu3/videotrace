#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os
import time
import shutil
import redis
import cv2
import imutils
import sys
from redis import Redis


def proc(fs,pt,pt1):
    for f in fs:
        ff = os.path.join(pt,f)
        ffid = f.split('-')[1]
        pw='/home/wlw/ffmpeg/bg/njue-'+ffid+'-bg.jpg'
        if  os.path.isfile(pw):
	    ch(f,ff,pw,pt1)
        else:
	    shutil.move(ff,pw)
        #print ff, os.stat(ff)
        #os.remove(ff)
    pass

def ch(f,pic,bg,pt1):
    num=0
    img1=cv2.imread(pic)
    img2=cv2.imread(bg)
    img3=imutils.resize(img1,width=500)
    img4=imutils.resize(img2,width=500)
    gray=cv2.cvtColor(img3,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(5,5),0)
    gray2=cv2.cvtColor(img4,cv2.COLOR_BGR2GRAY)
    gray2=cv2.GaussianBlur(gray2,(5,5),0)
    frame=cv2.absdiff(gray,gray2)
    (h,w)=frame.shape
    for i in range(h):
        for j in range(w):
	    if frame[i,j]>25:
		num+=1
    if float(num)/(w*h)<0.05:
        os.remove(pic)
    else:     
	cv2.imwrite(bg,img1)
        ffid = f.split('-')[1]
        t1=os.path.getctime(pic)
	t2=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(t1))
        newname=ffid+'-'+t2+'.jpg'
        #print newname
	ff1= os.path.join(pt1,newname)
        shutil.move(pic,ff1)
        fpw='/home/wlw/ffmpeg/img2'
	mod(newname,fpw)


def mod(filename,fpw):
    ffid=filename.split('-')[0]
    year=filename.split('-')[1]
    month=filename.split('-')[2]
    day=filename.split('-')[3]
    oth=filename.split('-')[4]
    hour=oth.split('_')[0]
    tdir=os.path.join(fpw,ffid)
    mdir=os.path.join(fpw,ffid)
    if  os.path.isdir(tdir):
        pass
    else:
        os.mkdir(tdir)   
    tdir=os.path.join(tdir,year)
    mdir=os.path.join(mdir,year)
    if os.path.isdir(tdir):
	pass
    else:
        os.mkdir(tdir)   
    tdir=os.path.join(tdir,month)
    mdir=os.path.join(mdir,month)
    if os.path.isdir(tdir):
	pass
    else:
        os.mkdir(tdir)   
    tdir=os.path.join(tdir,day)
    mdir=os.path.join(mdir,day)
    if  os.path.isdir(tdir):
        pass
    else:
        os.mkdir(tdir)  
    tdir=os.path.join(tdir,hour)
    if os.path.isdir(tdir):
        pass
    else:
        os.mkdir(tdir)  
    name=tdir+'/'+filename
    mdir=mdir+'/'
    shutil.move(os.path.join(fpw,filename),name)
    ff2=os.path.join('/home/wlw/ffmpeg',name)
    ff4=os.path.join('/home/wlw/ffmpeg',mdir)
    time1=filename.split('-',1)[1]
    time=time1.split('.')[0]
    ff3=ff2+'|'+ffid+'|'+time+'|'+ff4
    print ff3
    r = redis.Redis(host='127.0.0.1', port=6379) 
    r.lpush('test',ff3)
    

def read10(pt):
    fid = {}
    pt1 = '/home/wlw/ffmpeg/img2'
    while True:
        af = os.listdir(pt)
        for f in af:
            cid = f.split('-')[1]
            if cid in fid:
                if not f in fid[cid]:
                    fid[cid].append(f)
            else:
                fid[cid]=[f]
        for c in fid:
            if len(fid[c])>10:
                proc(fid[c],pt,pt1)
                fid[c] = []
        #print fid
        time.sleep(2)
        #break

    pass

def main():
    redis = Redis(host='127.0.0.1', port=6379)
    #while True:
   	#time.sleep(1)
    res = redis.rpop('test')
    if res == None:
       	pass
    else:
       	print str(res) 
    read10('/home/wlw/ffmpeg/img1')
    pass

if __name__ == '__main__':
    main()

