#!/usr/bin/python3
import socket
import sys
import select

server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
names = []
Liste_clients = [server]
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #Pour éviter les problèmes de 'Address already in use'


PORT=7777

server.bind(("",PORT))
server.listen(1)

print("Welcome to Chat Server")

indice_nom = 0

def MSG(datas):
    global indice_nom,name,name
    if datas[0] == "MSG":
        datas = datas[1:]
        name = '"' + adresseclient + ':' + portclient + '"'
        for i in range(len(names)):
            if int(portclient) == names[i]:
                name = names[i+1]
                indice_nom = i + 1

        name = "["+name+"] "
        for j in range(len(Liste_clients)):
            if j != 0 and Liste_clients[j]!=sender:
                info = " ".join(datas)
                message = name + info
                if info != "":
                    Liste_clients[j].sendall((message+"\n").encode("utf-8"))
                else:
                    Liste_clients[j].sendall("".encode("utf-8"))
    else:
        return 
    

def NICK(datas):
    global names
    if datas[0] == "NICK":
        for i in range(len(names)):
            #print("port",portclient,"names:",i,names[i], "taille",len(names), type(names[i]), type(int(portclient)), names[i]==int(portclient))
            if names[i]==int(portclient):
                names[i+1]=datas[1]
        print('client '+'"'+adresseclient+':'+portclient+'"'+' => '+'"'+datas[1]+'"')
        datas[0] = "MSG"
        datas[1:] = ""
        MSG(datas)
    else:
        return    

def QUIT(datas,i):
    global indice_nom
    if datas[0] == "QUIT":
        datas[0] = "MSG"
        MSG(datas)
        print('client disconnected '+'"'+names[indice_nom]+'"')
        names.pop(indice_nom-1)
        names.pop(indice_nom-1)
        Listes[i].close()
        Liste_clients.remove(Listes[i])
    else:
        return

def NAMES(datas):
    msg = ""
    if datas[0] == 'NAMES':
        list_server = []
        for i in range(0,len(names),2):
            list_server.append(names[i+1])

        for i in range(len(names)):
                if names[i] == int(portclient):
                    msg = ("[server] "+" ".join(list_server)+"\n")
                    msg = msg.encode('UTF-8')
        for j in range(len(Liste_clients)):
            if Liste_clients[j] == sender:
                Liste_clients[j].sendall(msg)
    else:
        return

def KILL(datas):
    global Listes, Liste_clients, names
    killed = 0
    if datas[0]=="KILL":
        i = names.index(datas[1])
        msg = str(datas[2:])
        for e in range(1,len(Liste_clients)):
            if Liste_clients[e].getpeername()[1]==names[i-1]:
                killed = e

        Liste_clients[e].sendall(str(" ".join(datas[2:])).encode('utf-8'))
        names.pop(i-1)
        names.pop(i-1)
        Liste_clients[e].close()
        Liste_clients.remove(Liste_clients[e])
    else:
        return

while True:
    Listes,_,_ = select.select(Liste_clients,[],[])

    for i in range(len(Listes)):

        if Listes[i] == server:
            client, b = server.accept()
            Liste_clients.append(client)
            names.append(b[1])
            names.append(b[0])
            for j in range(len(Liste_clients)):
                if j != 0 and Liste_clients[j] != Listes[i]:
                    adresseclient = str(b[0])
                    portclient = str(b[1])
                    name = ('client connected ' + '"' + adresseclient + ':' + portclient + '"' + '\n')
                    name = name.encode("utf-8")
                    Liste_clients[j].sendall(name)
            print(name.decode("utf-8"),end = "")
        else:

            data = Listes[i].recv(1500)
            sender = Listes[i]

            b = sender.getpeername()
            adresseclient = str(b[0])
            portclient = str(b[1])
            data = data.decode("utf-8")
            datas = data.split()

            if len(datas) == 0:
                Listes[i].close()
                Liste_clients.remove(Listes[i])

            elif (datas[0]!="NICK" and datas[0]!="MSG" and datas[0]!="QUIT" and datas[0]!="KILL" and datas[0]!="NAMES"):
                msg = "Invalid command"
                sender.sendall(msg.encode("UTF-8"))
                
            else:
                MSG(datas)
                NICK(datas)
                QUIT(datas,i)
                NAMES(datas)
                KILL(datas)

server.close()