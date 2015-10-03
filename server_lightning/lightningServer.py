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



	
host = 'localhost'
port = 8013
address = (host, port)
serversock = socket.socket()
serversock.bind(address)
serversock.listen(10)

##receive fileList.dat
print 'Waiting For Connection..\n'
clientsock, addr = serversock.accept()  #Receive the file that contains the files that the client will send to server
fileOpen = open("fileList.dat","wb")
print 'Connection Established From: ', addr
print '\n'
l = clientsock.recv(1024)
while (l):
        fileOpen.write(l)
        l=clientsock.recv(1024)
fileOpen.close()
clientsock.close() #The file received completely now you parse this file in order to receive one by one the files of the folder


##open fileList.dat and receive files one by one
import cPickle
print "Received fileList.dat so that server knows what to expect for...\n"
with open("fileList.dat","rb") as inputData:
    filenames = cPickle.load(inputData)
print "Now Receive files one by one...\n"
for x in range(len(filenames)):
    filename = filenames[x]
    print "filename, timeOfChange, examDate", filename.filename, filename.modificationDate, filename.examinationDate
    clientsock, addr = serversock.accept()
    fileOpen = open(filename.filename+'',"wb")
    print 'Receiving file ', filename.filename
    print "\n"
    l = clientsock.recv(1024)
    print l
    while (l):
        fileOpen.write(l)
        l=clientsock.recv(1024)
    fileOpen.close()
    clientsock.close()
	
print "All files received...\n"



