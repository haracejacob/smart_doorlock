#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 01:03:14 2017

@author: kim
"""
#detect face
#save image
#CNN
#Output

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
import glob
import numpy as np
import cv2

class camera :
    def __init__(self,id) :
        #self.flag = 0   #0:detect -1:not detect
        self.CAM_ID = id
        self.IMGDIR = './face/'
        self.IMGIDX = 0
        self.face_cascade = cv2.CascadeClassifier()
        self.eye_cascade = cv2.CascadeClassifier()
        self.face_cascade.load('./haarcascade_frontalface_default.xml')
        self.eye_cascade.load('./haarcascade_eye.xml')
        self.img_input = 0
        
    def set_camera(self) :
        self.cap = cv2.VideoCapture(self.CAM_ID) #카메라 생성
        if self.cap.isOpened() == False: #카메라 생성 확인
            print 'Can\'t open the CAM(%d)' % (self.CAM_ID)
            return -1
        print 'camera opened'

        cv2.namedWindow('Face')

    def show_camera(self) :
        while(True) :
            ret, frame = self.cap.read()
            tempframe = frame
            
            grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            grayframe = cv2.equalizeHist(grayframe)
        
            faces = self.face_cascade.detectMultiScale(grayframe, 1.1, 1, 0, (30, 60))
            if faces != () :
                largest_img = np.where(faces[:,3] == max(faces[:,3]))
                x,y,w,h = np.split(faces[largest_img[0][0]][:], 4)
                x -= 5
                y -= 5
                w += 10
                h += 10
                
                face_colorframe = frame[y:y+h, x:x+w]
                face_tempframe = tempframe[y:y+h, x:x+w]
                face_grayframe = grayframe[y:y+h, x:x+w]
                self.IMGIDX += 1
                self.IMGIDX %= 100
                img_name = self.IMGDIR + 'face%d.jpg'%self.IMGIDX
                
                cv2.imwrite(img_name, face_tempframe)
                
                eyes = self.eye_cascade.detectMultiScale(face_grayframe)
                
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3, 4, 0)
                cnt = 0
                for (ex,ey,ew,eh) in eyes:
                    if (h/3) > ey :
                        cv2.rectangle(face_colorframe,(ex,ey),(ex+ew,ey+eh),(0,255,255),2)
                        cnt+=1
            
            cv2.imshow('Face',frame)
            key = cv2.waitKey(100)
            if key == 27: #ESC KEY
                break
            if key == 32: #SPACE KEY / DETECT
                print 'start detect'
                if cnt > 0 :
                    print 'success'
                    self.img_input = self.IMGDIR + 'face%d.jpg'%self.IMGIDX
                    #self.img_input = cv2.imread(self.IMGDIR + 'face%d.jpg'%self.IMGIDX)
                    #self.img_input = cv2.resize(self.img_input, (227,227))
                    break
                else:
                    print 'false'
                    continue
   
    def del_camera(self) :
        #close the window
        self.cap.release()
        cv2.destroyWindow('Face')
        print 'del camera success'    
 
"""Main"""
#detect_pace()
video = glob.glob('/dev/video*')
cam = camera(int(video[0][-1]))
print 'init success'

cam.set_camera()
cam.show_camera()
cam.del_camera()
