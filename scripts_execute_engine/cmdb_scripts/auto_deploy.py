import subprocess

subprocess.check_output('touch testfile', stderr=subprocess.STDOUT, shell=True)







