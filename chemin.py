#!/usr/bin/env python3
def chdir(path, folder):
    return path+"/"+folder

def previous(path):
    temp = ""
    for i in path.split("/")[1:-1]:
        temp += "/"+i
    return temp
