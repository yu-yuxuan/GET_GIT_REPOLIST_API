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
    token=input('Enter token here: ') # "149***************c8d"
    username=input('Enter username here: ') #yu-yuxuan
    type=input('Enter type (repos, starred, subscriptions) here: ') #
    if token=="":
        url="https://api.github.com/users/%s/%s?per_page=100"  % (username,type)
    else:
        url="https://api.github.com/users/%s/%s?access_token=%s&per_page=100"  % (username,type,token)

    # https://api.github.com/users/yu-yuxuan/starred?per_page=100
    # https://api.github.com/users/yu-yuxuan/subscriptions?per_page=100
    allProjects     = urlopen(url)
    allProjectsDict = json.loads(allProjects.read().decode())
    for thisProject in allProjectsDict:
        try:
            thisProjectURL  = thisProject['ssh_url']
            print(thisProjectURL)
            with open(filename, "a") as myfile:
                myfile.write(thisProjectURL+ '\n')
        except Exception as e:
            print("Error on %s: %s" % (thisProjectURL, e.strerror))
