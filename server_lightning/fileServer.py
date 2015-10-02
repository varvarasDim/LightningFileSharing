import socket               # Import socket module
import sys
import datetime
import time
"""mylist = []
today = datetime.date.today()
mylist.append(today)

dateAndTime = time.strftime("%Y-%m-%d %H:%M:%S")

s = socket.socket()         # Create a socket object

port = 30000                # Reserve a port for your service.
s.bind(('', port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
    print ('STARTED')
    c, addr = s.accept()     # Establish connection with client.
    print('BLOCKED')
    print('Got connection from', addr)
    dateAndTime = time.strftime("%Y-%m-%d %H:%M:%S")
    c.send(('Thank you for connecting '+str(dateAndTime)).encode('utf-8'))
    c.close()                # Close the connection
	"""


class FileName:
    def __init__(self, filename, modificationDate, examinationDate):
        self.filename = filename
        self.modificationDate = modificationDate
        self.examinationDate = examinationDate



	
HOST = 'localhost'
PORT = 8013
BUFSIZE = 1024
ADDR = (HOST, PORT)
serversock = socket.socket()
serversock.bind(ADDR)
serversock.listen(10)

##receive fileData.dat
#while True:
print 'Waiting For Connection..\n'
clientsock, addr = serversock.accept()
fileOpen = open("fileData.dat","wb")
print 'Connection Established From: ', addr
print '\n'
l = clientsock.recv(1024)
while (l):
        fileOpen.write(l)
        l=clientsock.recv(1024)
fileOpen.close()
clientsock.close()
##open fileData.dat and receive files
import cPickle
print "Receive fileData.dat so that server knows what to expect for...\n"
with open("fileData.dat","rb") as inputData:
    obj = cPickle.load(inputData)
print "Receive files one by one...\n"
for x in range(len(obj)):
    tempFileName = obj[x]
    print "filename, timeOfChange, examDate", tempFileName.filename, tempFileName.modificationDate, tempFileName.examinationDate
    clientsock, addr = serversock.accept()
    fileOpen = open(tempFileName.filename+'',"wb")
    print 'Receiving file ', tempFileName.filename
    print "\n"
    l = clientsock.recv(1024)
    print l
    while (l):
        fileOpen.write(l)
        l=clientsock.recv(1024)
    fileOpen.close()
    clientsock.close()



