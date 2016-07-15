#!/usr/bin/python
import sys, str
from socket import *


def main (args):
	# Read init parameters
	parametersFilename = sys.argv ()
	inputDir, outputDir, nCpus = readParameters (parametersFilename)

	port = 52002
	 
	sock = socket()
	host = 'localhost' # '127.0.0.1' can also be used
	#Connecting to socket
	sock.connect((host, port)) #Connect takes tuple of host and port
	sock.send('STT_SUBSCRIBING:%s:%s:%s:%s:%s' % 
	           (host, port, inputDir, outputDir, nCpus))

	#Infinite loop to keep client running.
	while True:
		data = sock.recv(1024)
		print data
	 
	sock.close()

def readParameters (parametersFilename):
	params    = map (str.strip, open (parametersFilename).readlines())
	inputDir  = params[0].split(":")[1]
	outputDir = params[1].split(":")[1]
	nCpus     = params[1].split(":")[1]
	return  (inputDir, outputDir, nCpus)

#------------------------------------------------
if not __name__=="__main__":
	main (sys.argv)
