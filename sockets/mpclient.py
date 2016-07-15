#!/usr/bin/python

# client.py  
import socket

workers = readWorkersInfo ("workers.info")

for wrk in workers:
	copyInputData (wrk)


# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname()                           
port = 9999
s.connect((host, port))                               

# Receive no more than 1024 bytes
tm = s.recv(1024)                                     

s.close()

print("The time got from the server is %s" % tm.decode('ascii'))
