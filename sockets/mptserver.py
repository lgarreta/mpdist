#!/usr/bin/python
 
# Import all from module socket
from socket import *
#Importing all from thread
from thread import *
 
# Defining server address and port
host = ''  #'localhost' or '127.0.0.1' or '' are all same
port = 52002 #Use port > 1024, below it all are reserved
 
#Creating socket object, binding, and listening at the address.
sock = socket()
sock.bind((host, port))
sock.listen(5) #5 denotes the number of clients can queue
 
def clientThread(conn):
	# The function does not terminate and thread does not end.
	while True:
		#Receiving from client
		data = conn.recv(1024) # 1024 stands for bytes of data to be received
		info = data.split (":")
		if info [0] == "STT_SUBSCRIBING":
			print "Subscribing worker: %s" % info [1]
			#Sending message to connected client
			conn.send('Hi! I am server\n') #send only takes string
 
while True:
	# Accepting incoming connections
	conn, addr = sock.accept()
	# Creating new thread calling clientThread function 
	# and passing the tuple arguments (conn,) as argument to it
	start_new_thread(clientThread,(conn,)) 
 
conn.close()
sock.close()
