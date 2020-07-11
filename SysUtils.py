#=========================================================================
#	SysUtils.py
#	Author: Raul Rojas
#	Contact: rrojas994@gmail.com
#	Description: 
#		Provides some utilities that involve the system or OS operations.
#=========================================================================

import subprocess

#------------------------------------------------------------
#	runsSys()
#		Description: Executes a system command and returns 
#           the output from stdout. Raises a SystemError 
#           exception if the command outputs to stderr.
#------------------------------------------------------------
def runSys(inputCommand: str):
    out = subprocess.Popen(inputCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = out.communicate()
    if(stderr):
        errorMsg = f'An error occured when running system command: "{inputCommand}"\n' + stderr
        raise SystemError(errorMsg)
    return stdout.decode('utf-8').strip()
