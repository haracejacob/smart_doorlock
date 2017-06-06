import sys
import socket
import select
#import time
import Queue
#from threading import Timer

HOST = ''
SOCKET_LIST = []
OUTPUT_LIST = []
message_queues = {}
PORT = 9009 

# Settable parameters
NUM_OF_NODES = 10 # The maximum number of nodes
BANDWIDTH = 10000 # 1000 = 1KB, in turn, 10000  = 10KB (B/SEC)
MTU = 1000 # Maximum Transmit Unit for this medium (B)
RECV_BUFFER = 2*MTU # Receive buffer size
PDELAY = 0.1 # Propagation delay (s)

def medium():

    medium_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    medium_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    medium_socket.bind((HOST, PORT))
    medium_socket.listen(NUM_OF_NODES)

    # Add medium socket object to the list of readable connections
    SOCKET_LIST.append(medium_socket)

    global STATUS # Status of Medium : I -> Idle, B -> Busy

    print("Medium is Activated (port:" + str(PORT) + ") ")

    while 1:
      try:
        # Get the list sockets which are ready to be read through select
        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, OUTPUT_LIST, [], 0)

        for sock in ready_to_read:
          # A new connection request received
          if sock == medium_socket: # 0.0.0.0 : 9009 (sock)
            sockfd, addr = medium_socket.accept()
            SOCKET_LIST.append(sockfd)
            print("Node (%s, %s) connected" % addr)
            message_queues[sockfd] = 'QUIT'
            OUTPUT_LIST.append(sockfd)
          # A message from a node, not a new connection
          else: # 127.0.0.1 : 9009 (sock)
            try:
              # Receiving packet from the socket.
              packet = sock.recv(RECV_BUFFER)
              if packet:
                # Check medium here!
                message_queues[sock] = 'OPEN'
                # Add output channel for response
                if sock not in OUTPUT_LIST:
                    OUTPUT_LIST.append(sock)
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
        print 1
        print ready_to_write
        for sock in ready_to_write:
          try:
            next_msg = message_queues[sock]
            del message_queues[sock]
          except:
            # No messages waiting so stop checking for writability.
            print ('output queue for', sock.getpeername(), 'is empty')
            OUTPUT_LIST.remove(sock)
          else:
            print ('sending "%s" to %s' % (next_msg, sock.getpeername()))
            sock.send(next_msg)
      except:
        print('\nMedium program is terminated')
        medium_socket.close()
        sys.exit()

if __name__ == "__main__":
    sys.exit(medium())
