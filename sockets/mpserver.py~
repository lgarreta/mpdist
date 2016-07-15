#!/usr/bin/python
# mpserver.py 
import socket                                         
import time

# Create, bind, and listen a socket object: AF_INET, SOCK_STREAM
serverSocket = socket.socket()
host = socket.gethostname()                           
port = 9999                                           
serverSocket.bind((host, port))                                  
serverSocket.listen(5)                                           

while True:
    # Establish a connection
    clientsocket,addr = serverSocket.accept()      
    print("Got a connection from %s" % str(addr))
	commandStr = serverSocket.recv (1024)
	prog, inDir, outDir, nCpus, log = commandStr.split (":")
	print ("Running >>> %s" % commandStr)
	os.system (commandStr)
	serverSocket.send ("Finished >>> %s" % commandStr)

clientsocket.close()
