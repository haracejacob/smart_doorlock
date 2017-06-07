#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 01:08:55 2017

@author: kim
"""

import sys
import socket
import time

# Settable parameters
MTU = 1000 # Maximum Transmit Unit for this medium (B)
RECV_BUFFER = 2*MTU # Receive buffer size

def node():
    s = connect_to_medium() # Connection
    print 'send packet'
    s.send("2")
    packet = s.recv(RECV_BUFFER)
    print packet
    s.close()
    sys.exit()
   
# Connect a node to medium ----- recommand not to modify
def connect_to_medium():
  host = '127.0.0.1' # Local host address
  #host = '192.168.43.243'
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



if __name__ == "__main__":
    sys.exit(node())

