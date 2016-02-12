#!/usr/bin/python3
from urllib.request import urlopen
import json
import os, errno

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured

if __name__ == '__main__':
    filename=input('Enter file name here: ') # "README.org"
    silentremove(filename)
    url=input('Enter url here: ') # "https://******/api/v3/groups/1?private_token=36v********************RGy"
    allProjects     = urlopen(url)
    allProjectsDict = json.loads(allProjects.read().decode())
    for thisProject in allProjectsDict['projects']:
        try:
            thisProjectURL  = thisProject['ssh_url_to_repo']
            print(thisProjectURL)
            with open(filename, "a") as myfile:
                myfile.write(thisProjectURL+ '\n')
        except Exception as e:
            print("Error on %s: %s" % (thisProjectURL, e.strerror))
