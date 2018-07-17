#! /usr/bin/env python3

import os
import subprocess
import socket
import sys


#
#Checking if there is internet connection for downloading the various packages
#
check = 'www.google.com'
def checkinternet(hostname):
    try:
        host = socket.gethostbyname(hostname)
        s=socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


def packinstalled():
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    inst = [r.decode().split('==')[0] for r in reqs.split()]
    if 'geopy' in inst:
        return True


#
#Updating the apt function
def aptUpdate():
    os.system('sudo apt update')
    return 0



#                                                                
# Install the NFS server package                                                   
def installNFS():
    os.system('sudo apt-get install nfs-kernel-server')
    return 0

#                                                                
# Install the fping package                                                   
def installfping():
    os.system("sudo apt-get install fping -y")
    return 0

#                                                                
# Install the portmap package 
def installportmap():
    os.system('sudo apt-get install portmap')
    return 0


    
#
#creating a directory in the server to use shared location:
'''
Please take directory name from user
'''
def shareddir(dirname):
    cmd1 = ('sudo chown pi:pi '+ dirname)
    if os.path.exists(dirname):        
        os.system(cmd1)
        
    else:
        location = dirname
        cmd = ('sudo mkdir '+ location)
        os.system(cmd)
        os.system(cmd1)

#
#editing the /etc/hosts.deny file
def editHostsDeny():
    filename = open('/etc/hosts.deny', 'a')
    write = 'rpcbind mountd nfsd statd lockd rquotad : ALL\n'
    cont = check(write,'/etc/hosts.deny')
    if cont:
        return True
    else:
        filename.write(write)
        filename.close()
    return True
#
#
#Adding files to the /etc/hosts.allow file
def editHostsAllow(address):
    filename = open('/etc/hosts.allow', 'a')
    write = 'rpcbind mountd nfsd statd lockd rquotad : 127.0.0.1 : allow\n'
    write1 = 'rpcbind mountd nfsd statd lockd rquotad : ' + address + ': allow\n'
    write2 = 'rpcbind mountd nfsd statd lockd rquotad : ALL : deny\n'
    c1=check(write,'/etc/hosts.allow')
    c2=check(write2,'/etc/hosts.allow')
    if c1 == False:
        filename.write(write)
        
    if c2==False:
        filename.write(write2)
        
    cont = check(write1,'/etc/hosts.allow')
    if cont:
        return True
    else:
        filename.write(write1)
        filename.close()
    return True

##********************************************
#Opening the directory
def openfolder(directory):
    cmd = "xdg-open " + directory
    os.popen(cmd)

##
##
#Checking the hosts.deny and exports files
def check(text,dir):
    datafile = open(dir,'r')
    for line in datafile:
        if text in line:
            return True
    return False
################################################


#
#editing the /etc/exports file
'''
please take note of the directory from the user
'''
def editExports(dirname, address):
    filename = open('/etc/exports', 'a')
    write = (dirname + "\t" + address + "/17" + "(rw,all_squash,subtree_check,anonuid=1001,anongid=1001)\n")
    cont = check(write,'/etc/exports')
    if cont:
        return
    else:
        filename.write(write)
        filename.close()
    return True
#################################################   

def updatefs():
    os.system('sudo exportfs -ra')
    return 0

def restartnfs():
    os.system('sudo systemctl restart nfs-kernel-server')
    return 0

#****************************************************************************
#                                                                
# Install the nfs-common package 
def installnfscommon():
    os.system('sudo apt install nfs-common')
    return 0

#
#creating a directory in the client to mount the server drive:
'''
Please take directory name from user
'''
def makemountdir(dirname):
    cmd = 'mkdir ' + dirname
    if os.path.exists(dirname):        
        return
        
    else:
        location = dirname
        cmd = ('mkdir '+ location)
        os.system(cmd)

#
#editing the /etc/fstab file
def editfstab(serip, serdir, moutd):
    filename = open('/etc/fstab', 'a')
    write = serip + ':' + serdir + '\t' + moutd + '\tnfs rw,async,hard,intr,noexec 0 0\n'
    cont = check(write,'/etc/fstab') 
    if cont:
        return True
    else:
        filename.write(write)
        filename.close()
    return True

#
#mounting the directory to see the server files
def mountdrive(dirname):
    cmd= 'sudo mount ' + dirname
    os.system(cmd)
    

#****************************************************************************
#
#
#
#
#
#
#
#Creating the main to call the various functions
def set_server(clientip,serverdirectory):    
    inter = checkinternet(check) #Checking if there is internet connection and assigning it to $inter
    if inter:         
        aptUpdate()       #Update the package references:
        installNFS()      #Install the NFS server package
        installportmap()  #Install the Portmapper package
        installfping()    #Install the fping package to get ip addresses
    
    
    editHostsDeny()       #Editing the /etc/hosts.deny
    
    #clientip = input("Please input client ip address")
    #serverdirectory = input("Please input the directory for NFS server location")
    
    editHostsAllow(clientip)    #adding the client ip to the hostallow file
    
    shareddir(serverdirectory)  #Creating a directory to serve the nfs location
    
    editExports(serverdirectory,clientip) # Adding the directory to the exports file
        
    updatefs()
    restartnfs()
    
    
#
#
#
#function for the client system    
def set_client(serverip,serverdirectory,moudir):    
    inter = checkinternet(check) #Checking if there is internet connection and assigning it to $inter
    if inter:         
        aptUpdate()          #Update the package references:
        installnfscommon()   #Install the NFS server package
        installfping()       #Install the fping package to get ip addresses
    
    
    
    #serverip = input("Please input server ip address")
    #serverdirectory = input("Please input the directory for NFS server location")
    #moudir = input("Please input the directory to mount the server drive")
    
    makemountdir(moudir)
    
    editfstab(serverip, serverdirectory, moudir)
    
    mountdrive(moudir)


