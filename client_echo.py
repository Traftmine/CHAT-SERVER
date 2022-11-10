#!/usr/bin/python3
import socket
import sys

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

port = 7777
host = ""

s.connect((host,port))

while True:

    line = sys.stdin.readline() 
    if line == "\n" or line == "":
        print("JAQUITTE")
        break

    s.sendall(line.encode("UTF-8"))
    msg = s.recv(1500)
    print( msg.decode("utf-8"))
    
    quit=""
    count=0
    for lettre in line:
        if count<4:
            quit=quit+lettre
            count+=1
    if quit=="QUIT":
        print("JAQUITTE")
        break
s.close()