#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 01:08:55 2017

@author: kim
"""

import sys
import socket
import select
from threading import Timer

import serial

ard = serial.Serial('/dev/ttyACM0', 9600)

# Settable parameters
MTU = 1000 # Maximum Transmit Unit for this medium (B)
RECV_BUFFER = 2*MTU # Receive buffer size

def node():
    s = connect_to_medium() # Connection
    sys.stdout.write('Press ENTER key for transmitting a packet or type \'quit\' to end this program : '); sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])
        print ready_to_read
        for sock in ready_to_read:
            if sock == s:
              # Incoming data packet from medium
              packet = sock.recv(RECV_BUFFER) # Recive a packet
              data = extract_data(packet) # Extract data in a packet
              if not data:
                print('\nDisconnected')
                sys.exit()
              else:
                print("\nReceive a packet : %s" % data)
		if(data == 'OPEN') :
		  ard.write('OPEN')
		  transmit(s, 'ok')
		if(data == 'QUIT') :
		  s.close()
		  sys.exit()
            else:
              """
               here we should write switch condition and face detection function
              """
# Connect a node to medium ----- recommand not to modify
def connect_to_medium():
  #host = '127.0.0.1' # Local host address
  host = '192.168.43.243'
  port = 9009 # Medium port number
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  s.settimeout(2)
  try:
    s.connect((host, port))
  except:
    print('Unable to connect')
    sys.exit()

  print('Connected. You can start sending packets')

  return s


# Make and transmit a data packet
def transmit (s, trans_data):

  packet = trans_data 

  if len(packet) > MTU:
    print('Cannot transmit a packet -----> packet size exceeds MTU')
  else:
    packet = packet + '0'*(MTU-(len(trans_data)))
    s.send(packet)
    print('Transmit a packet')

# Extract data
def extract_data(packet):
  i=0
  for c in packet:
    if c == '0':
      break
    else:
      i=i+1
      continue

  data = packet[0:i]
  return data

if __name__ == "__main__":
    sys.exit(node())

