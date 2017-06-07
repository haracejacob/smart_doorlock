import sys
reload(sys)  
sys.setdefaultencoding('utf8')

import socket
import select
import time
import os
from threading import Timer

import glob
import numpy as np
import cv2

#import serial

#ard = serial.Serial('/dev/ttyACM0', 9600)

HOST = ''
SOCKET_LIST = []
PORT = 9009 

# Settable parameters
NUM_OF_NODES = 10 # The maximum number of nodes
MTU = 1000 # Maximum Transmit Unit for this medium (B)
RECV_BUFFER = 2*MTU # Receive buffer size

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
        self.face_list = []
        self.face_result = 0
        
    def set_camera(self) :
        self.cap = cv2.VideoCapture(self.CAM_ID) #카메라 생성
        if self.cap.isOpened() == False: #카메라 생성 확인
            print 'Can\'t open the CAM(%d)' % (self.CAM_ID)
            return -1
        print 'camera opened'

        cv2.namedWindow('Face')

    def show_camera(self) :
        while(True) :
            cnt = 0
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
                        
            if cnt == 2 :
                self.face_list.append(img_name)
            
            if len(self.face_list) == 5 :
                break
            
            cv2.imshow('Face',frame)
            key = cv2.waitKey(10)
   
    def del_camera(self) :
        #close the window
        self.cap.release()
        cv2.destroyWindow('Face')
        print 'del camera success'
        
    def check_face(self) :
        import requests
        import json
        print self.face_list
        url = "http://127.0.0.1:5000/classify_rest"
        
        result = 0
        for idx in range(len(self.face_list)) :
            files = {'imagefile' : open(self.face_list[idx],"rb")}
            
            r = requests.post(url, files = files)

            data = json.loads(r.text)
            result += int(data['val'])
            
        if result >= 3 :
            return 1
        else :
            return 0

def medium():
    date = round(time.time())
    medium_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    medium_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    medium_socket.bind((HOST, PORT))
    medium_socket.listen(NUM_OF_NODES)

    # Add medium socket object to the list of readable connections
    SOCKET_LIST.append(medium_socket)
    
    print("Medium is Activated (port:" + str(PORT) + ") ")

    while 1:
      try:
        # Get the list sockets which are ready to be read through select
        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)

        for sock in ready_to_read:
          # A new connection request received
          if sock == medium_socket: # 0.0.0.0 : 9009 (sock)
            sockfd, addr = medium_socket.accept()
            SOCKET_LIST.append(sockfd)

            # naming the nodes an alphabet like A, B, C...
            print("Node (%s, %s) connected" % addr)

          # A message from a node, not a new connection
          else: # 127.0.0.1 : 9009 (sock)
            try:
              # Receiving packet from the socket.
          #####################################
          #### JONGHAP SULGAE PROJECT PART ####
          #####################################
              packet = sock.recv(RECV_BUFFER)
              if packet:
                data = packet.decode('utf-8')
                if data == "1_12345678":
		  #ard.write('OPEN')
                  print("ON")
		  sock.send("ok")
		  date = round(time.time())
		  # door open
                elif data == "2":
                  print("DATA")
		  sock.send(str(date))
		# send
            ###################################
            ###################################
            ###################################
              else:
                if sock in SOCKET_LIST:
                  print("Node (%s, %s) disconnected" % sock.getpeername())
                  SOCKET_LIST.remove(sock)
                  continue
	
            # Exception
            except:
              if sock in SOCKET_LIST:
                print("Error! Check Node (%s, %s)" % sock.getpeername())
                SOCKET_LIST.remove(sock)
              continue
        #ardiomp switch value get  
	if True :
	  video = glob.glob('/dev/video*')
	  cam = camera(int(video[0][-1]))
	  cam.set_camera()
	  cam.show_camera()
	  result = cam.check_face()
	  cam.del_camera()

	  if result == 1 :
	    print 'ok'
	  else :
	    print 'no'

      except:
        print('\nMedium program is terminated')
        medium_socket.close()
        sys.exit()


if __name__ == "__main__":
    sys.exit(medium())
