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
port = 8013

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
for filename in filenames:
    f.write(filename+'\t'++'\n')
f.close()
print folders
print filenames"""

##get metadata of file,serialize them and deserialize them
filenames=[]
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
        if filename != 'fileListLastAccess.dat' and filename != 'fileList.dat' and filename != 'lightningClient.py' :
            filenames.append(os.path.join(dirpath, filename))
currentFilesInFolder =[]
print "Extract MetaData of files...\n"
for filename in filenames:
    t=os.path.getmtime(filename)
    currentFilesInFolder.append(FileName(filename,datetime.datetime.fromtimestamp(t),datetime.datetime.now()))

##check if fileListLastAccess NOT exists (if TRUE means that it is the first time that the algorithm runs)
if not os.path.isfile("fileListLastAccess.dat"):
    print "Export file data to file fileList.dat...\n"
    with open("fileList.dat","wb") as outputData:
        cPickle.dump(currentFilesInFolder,outputData,cPickle.HIGHEST_PROTOCOL)
    ##send fileList.dat
    print "Send fileList.dat to server...\n"
    s = socket.socket()
    s.connect(("localhost",port))
    f=open("fileList.dat", "rb") 
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)
    f.close()
    s.close()
    #time.sleep(10)
    ##send each file
    print "Open fileList.dat to get filelist (DEBUG MODE)...\n"
    with open("fileList.dat","rb") as inputData:
        filenames = cPickle.load(inputData)
    print "Send files to server one by one..."
    for x in range(len(filenames)):
        filename = filenames[x]
        print "Sending file: "+ filename.filename +", timeOfChange: " + str(filename.modificationDate)+\
              ", examDate: " + str(filename.examinationDate)
        print "\n"
        s = socket.socket()
        s.connect(("localhost",port))
        f=open(filename.filename+'', "rb") 
        l = f.read(1024)
        while (l):
            s.send(l)
            l = f.read(1024)
        f.close()
        s.close()
    #save filelist to fileListLastAccess.dat
    print "Save fileListLastAccess.dat locally so that next time the client will know which files did he send...\n"
    with open("fileListLastAccess.dat","wb") as outputData:
        cPickle.dump(currentFilesInFolder,outputData,cPickle.HIGHEST_PROTOCOL)
else:
    #open fileListLastAccess
    fileNamesLA = []
    print "Open fileListLastAccess.dat so that you can read what server is being sent...\n"
    with open("fileListLastAccess.dat","rb") as inputData:
        fileNamesLA = cPickle.load(inputData)
    print "Create separate lists of new and old files...\n"
    filesInFolderOld = [] #list that will replace previous data in fileListLastAccess.dat
    filesInFolderNewOrUpdated = [] #list that will maintain only the new files or modified ones
    
    for fileX in currentFilesInFolder: 
         if any(x.filename == fileX.filename and x.modificationDate == fileX.modificationDate for x in fileNamesLA): #check if fileX is a new one or a modified one
            filesInFolderOld.append(fileX) #if it is old move it here
            print "    File "+fileX.filename+" is NOT a new File..."
         else:
            filesInFolderNewOrUpdated.append(fileX) #else move it to this list
            print "    File "+fileX.filename+" is a new File..."

            
    print "Export fileList.dat thatn contains only new or modified files...\n"
    with open("fileList.dat","wb") as outputData:
        cPickle.dump(filesInFolderNewOrUpdated,outputData,cPickle.HIGHEST_PROTOCOL)
    ##send fileList.dat
    print "Send fileList.dat to server one by one...\n"
    s = socket.socket()
    s.connect(("localhost",port))
    f=open("fileList.dat", "rb") 
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)
    f.close()
    s.close()
    ##send each file
    print "Open fileList.dat to get filelist (DEBUG MODE)...\n"
    with open("fileList.dat","rb") as inputData:
        filenames = cPickle.load(inputData)
    for x in range(len(filenames)):
        filename = filenames[x]
        print "Sending file: "+ filename.filename +", timeOfChange: " + str(filename.modificationDate) +\
              ", examDate: " + str(filename.examinationDate)
        print "\n"
        s = socket.socket()
        s.connect(("localhost",port))
        f=open(filename.filename+'', "rb") 
        l = f.read(1024)
        while (l):
            s.send(l)
            l = f.read(1024)
        f.close()
        s.close()
    print "Save fileListLastAccess.dat locally so that next time the client will know which files did he send...\n"
    filesInFolderOld = filesInFolderOld + filesInFolderNewOrUpdated ##merge the list with the new/modified files and list with the unchanged files
    #save filelist to fileListLastAccess.dat
    with open("fileListLastAccess.dat","wb") as outputData:
        cPickle.dump(filesInFolderOld, outputData,cPickle.HIGHEST_PROTOCOL)
            
      
    






    
    
