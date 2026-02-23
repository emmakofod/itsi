#### This is the client part
#
#
#
#
#
####

import socket 
import select 
import sys 
import pickle
import codecs
import time

from _thread import *


def send_data(sock,data,delimitter=b"!##2?3##!!!##!!!"):
    data=pickle.dumps(data)
    send_da=codecs.encode(data,"base64").strip()+delimitter
    sock.sendall(send_da)
    return 0

def rcv_data(sock,delimitter=b"!##2?3##!!!##!!!"):
    data=b""
    while not data.endswith(delimitter):
        data+=sock.recv(2048)
    data=codecs.decode(data[:-len(delimitter)],"base64")
    data=pickle.loads(data)
    return data

###############################################
class client():
    def __init__(self,ip_address="localhost", port=10000):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.ip_address = ip_address
        self.port = port 
        self.server.connect((self.ip_address, self.port)) 
        print(rcv_data(self.server))

    def login(self,username,password):
        send_data(self.server,"LOGIN:-:"+username+":#:"+password) 
        print(rcv_data(self.server))

    def getusers(self):
        send_data(self.server,"GETUSERS:-:xxxx") 
        print(rcv_data(self.server))

    def score(self):
        send_data(self.server,"SCORE:-:xxxx") 
        print(rcv_data(self.server))

    def question(self,num):
        send_data(self.server,"QUESTION:-:"+str(num)) 
        print(rcv_data(self.server))

    def answer(self,num,ans):
        send_data(self.server,"ANSWER:-:"+str(num)+":#:"+str(ans)) 
        print(rcv_data(self.server))

    def data(self,num):
        send_data(self.server,"DATA:-:"+str(num)) 
        rcv=rcv_data(self.server)
#        print(str(rcv_data(self.server)))
        return rcv
        
        

    def close(self):
        self.server.close()         



