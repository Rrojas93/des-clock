#!/usr/bin/python3
# -*- coding: utf-8 -*-

#=========================================================================
#	.uploadFiles.py
#	Author: Raul Rojas
#	Contact: rrojas994@gmail.com
#	Description: 
#		Uploads all files in this workspace to the appropraite locations 
#       on the raspberry pi. Created to make testing and deploying to the
#       Raspberry Pi as quick and painless as possible.
#=========================================================================

import os
import pysftp as sftp
import glob
import _secrets

secrets = _secrets.MySecrets()
scriptFilesPath = '/home/pi/rr/scripts/DeskClock/'
desktopPath = '/home/pi/Desktop/'
autoStartPath = '/etc/xdg/autostart/'
piIpAddress = secrets.rpi_ip_wlan_address # local ip address (from wifi connection) to access through ssh/sftp

cnopts = secrets.cnopts
ignore = [  # files to ignore when uploading
    'Settings.json' # will be created automatically with defaults if missing. 
    'uploadFiles.py'
]

def main():
    uploadAllFiles()
    print('File Upload Successful')

#------------------------------------------------------------
#	uploadAllFiles()
#		Description: Uploads all files to the Raspberry pi 
#           with two seperate sftp connections. First is 
#           using regular user to avoid ownership issues and
#           second connection with "root" user to upload 
#           files to system directories. 
#------------------------------------------------------------
def uploadAllFiles():
    try:
        # Open a connection as the normal user "pi" in the desired locations. 
        with sftp.Connection(host=piIpAddress, username='pi', password=secrets.rpi_pi_userPW, cnopts=cnopts) as con: 
            print('Opening Connection as user "pi"')
            fls = getScriptFiles()
            uploadFilesToPath(fls, targetPath=scriptFilesPath, sftpConnection=con)
            fls = getDesktopFiles()
            uploadFilesToPath(fls, targetPath=desktopPath, sftpConnection=con)
        # Open a connection as root to upload files in system directories.
        with sftp.Connection(host=piIpAddress, username='root', password=secrets.rpi_root_userPW, cnopts=cnopts) as con:
            print('Opening Connection as user "root"')
            fls = getAutostartFiles()
            uploadFilesToPath(fls, targetPath=autoStartPath, sftpConnection=con)
    except Exception as e:
        print('Unable to Connect. \nError:' + str(e))
            
#------------------------------------------------------------
#	uploadFilesToPath()
#		Description: Performs the upload with an already 
#           established connection. Will skip uploading files
#           that are listed under "ignore" global var.
#------------------------------------------------------------
def uploadFilesToPath(fls: list, targetPath: str, sftpConnection: sftp.Connection):
    print('Uploading files: ' + str(fls))
    for f in fls:
        if(f in ignore):
            print('File ignored: ' + f)
            continue
        destF=f.split('\\')[-1]
        try:
            sftpConnection.put(localpath=f, remotepath=targetPath + destF, confirm=True)
        except Exception as e:
            print('Unable to upload file: ' + str(f) + '\nError: ' + str(e))

# Gets all main script files
def getScriptFiles():
    fls = glob.glob('*.py', recursive=False)
    fls += glob.glob('*.sh', recursive=False)
    return fls

# gets DesktopFiles to place on the Desktop
def getDesktopFiles():
    fls = glob.glob('desktopFiles\\*.Desktop', recursive=False)
    return fls

# gets DesktopFiles and places them on the startup folder 
def getAutostartFiles():
    fls = glob.glob('autostartFiles\\*.Desktop', recursive=False)
    return fls

if __name__ == "__main__":
    main()