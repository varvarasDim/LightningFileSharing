"""import os.path
from os import listdir
from os.path import isfile,join
mypath = os.path.dirname(os.path.realpath(__file__))
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f))]


print onlyfiles
"""
import socket
import sys
import os
import time
import os.path
import os.path

import datetime


class FileName:
    def __init__(self, filename, modificationDate, examinationDate):
        self.filename = filename
        self.modificationDate = modificationDate
        self.examinationDate = examinationDate

    


import cPickle
PORT = 8013

"""#create directory hierarchy
homedir='.\HOME'
if not os.path.exists(homedir):
    os.mkdir(homedir)
for folder in folders:
    os.mkdir(os.path.join(homedir,folder))
    print os.path.join(homedir,folder)

f = open('files.txt','w')
for folder in folders:
    f.write(folder+'\n')
f.write('FILES'+'\n')
for filename in allfiles:
    f.write(filename+'\t'++'\n')
f.close()
print folders
print allfiles"""

##get metadata of file,serialize them and deserialize them
allfiles=[]
folders=[]

print "Begin to parse data folder data...\n"
for dirpath, dirnames, filenames in os.walk("."):
    #print "CHANGE DIRECTORY"
    for folder in dirnames:
        print "\n    Folder Found...",folder
        if folder != 'HOME':
            folders.append(os.path.join(dirpath,folder))
    for filename in filenames:
        print "\n    Files Found...!",filename
        if filename != 'fileDataLastAccess.dat' and filename != 'fileData.dat' and filename != 'printfilesindir.py' :
            allfiles.append(os.path.join(dirpath, filename))
fileNamesList =[]
print "Extract MetaData of files...\n"
for filename in allfiles:
    t=os.path.getmtime(filename)
    fileNamesList.append(FileName(filename,datetime.datetime.fromtimestamp(t),datetime.datetime.now()))

##check if fileDataLastAccess NOT exists (if TRUE means that it is the first time that the algorithm runs)
if not os.path.isfile("fileDataLastAccess.dat"):
    print "Export file data to file fileData.dat...\n"
    with open("fileData.dat","wb") as outputData:
        cPickle.dump(fileNamesList,outputData,cPickle.HIGHEST_PROTOCOL)
    ##send fileData.dat
    print "Send fileData.dat to server...\n"
    s = socket.socket()
    s.connect(("localhost",PORT))
    f=open("fileData.dat", "rb") 
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)
    f.close()
    s.close()
    #time.sleep(10)
    ##send each file
    print "Open fileData.dat to get filelist (DEBUG MODE)...\n"
    with open("fileData.dat","rb") as inputData:
        obj = cPickle.load(inputData)
    print "Send files to server one by one..."
    for x in range(len(obj)):
        tempFileName = obj[x]
        print "Sending file: "+ tempFileName.filename +", timeOfChange: " + str(tempFileName.modificationDate)+\
              ", examDate: " + str(tempFileName.examinationDate)
        print "\n"
        s = socket.socket()
        s.connect(("localhost",PORT))
        f=open(tempFileName.filename+'', "rb") 
        l = f.read(1024)
        while (l):
            s.send(l)
            l = f.read(1024)
        f.close()
        s.close()
    #save filelist to fileDataLastAccess.dat
    print "Save fileDataLastAccess.dat locally so that next time the client will know which files did he send...\n"
    with open("fileDataLastAccess.dat","wb") as outputData:
        cPickle.dump(fileNamesList,outputData,cPickle.HIGHEST_PROTOCOL)
else:
    #open fileDataLastAccess
    fileNamesLA = []
    print "Open fileDataLastAccess.dat so that you can read what server is being sent...\n"
    with open("fileDataLastAccess.dat","rb") as inputData:
        fileNamesLA = cPickle.load(inputData)
    print "Create separate lists of new and old files...\n"
    fileNamesListLAUpdated = [] #list that will replace previous data in fileDataLastAccess.dat
    fileNamesListUpdated = [] #list that will maintain only the new files or modified ones
    
    for fileX in fileNamesList: 
         if any(x.filename == fileX.filename and x.modificationDate == fileX.modificationDate for x in fileNamesLA): #check if fileX is a new one or a modified one
            fileNamesListLAUpdated.append(fileX) #if it is old move it here
            print "    File "+fileX.filename+" is NOT a new File..."
         else:
            fileNamesListUpdated.append(fileX) #else move it to this list
            print "    File "+fileX.filename+" is a new File..."

            
    print "Export fileData.dat thatn contains only new or modified files...\n"
    with open("fileData.dat","wb") as outputData:
        cPickle.dump(fileNamesListUpdated,outputData,cPickle.HIGHEST_PROTOCOL)
    ##send fileData.dat
    print "Send fileData.dat to server one by one...\n"
    s = socket.socket()
    s.connect(("localhost",PORT))
    f=open("fileData.dat", "rb") 
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)
    f.close()
    s.close()
    ##send each file
    print "Open fileData.dat to get filelist (DEBUG MODE)...\n"
    with open("fileData.dat","rb") as inputData:
        obj = cPickle.load(inputData)
    for x in range(len(obj)):
        tempFileName = obj[x]
        print "Sending file: "+ tempFileName.filename +", timeOfChange: " + str(tempFileName.modificationDate) +\
              ", examDate: " + str(tempFileName.examinationDate)
        print "\n"
        s = socket.socket()
        s.connect(("localhost",PORT))
        f=open(tempFileName.filename+'', "rb") 
        l = f.read(1024)
        while (l):
            s.send(l)
            l = f.read(1024)
        f.close()
        s.close()
    print "Save fileDataLastAccess.dat locally so that next time the client will know which files did he send...\n"
    fileNamesListLAUpdated = fileNamesListLAUpdated + fileNamesListUpdated ##merge the list with the new/modified files and list with the unchanged files
    #save filelist to fileDataLastAccess.dat
    with open("fileDataLastAccess.dat","wb") as outputData:
        cPickle.dump(fileNamesListLAUpdated, outputData,cPickle.HIGHEST_PROTOCOL)
            
      
    






    
    
