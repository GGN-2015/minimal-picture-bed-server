# this is a minimal version of ggntalk(client)

# ggntalk is a program based on "ggnsql".

# same basic message of the program, if you don't want your ggntalk go wrong, don't change the code following.

VERSION  = "Test Version 2.0(minimal)"
AUTHOR   = "GGN_2015"
SHIPDATE = "2020-08-16"

import time
import os
import socket
import traceback

def getfb(filename):
    ans = ""
    try:
        fi = open(filename, "rb")
        ans = fi.read()
        fi.close()
    except:
        print("[getfb] error when read.")
        print(traceback.format_exc())
        ans = "<file not found>"
    return ans

def enco(msg):
    if type(msg) == str:
        return msg.encode("utf-8")
    return msg

def csnd(msg, HOST,\
        PORT,\
        BUFSIZ): # try to connect with the server
    ADDR = (HOST, PORT)
    tcp = socket.socket(socket.AddressFamily.AF_INET,\
        socket.SOCK_STREAM)
    # tcp protocol, pay attention to the prefix of the const
    try:
        tcp.connect(ADDR)
    except:
        return "#error: can not connect to the server."
        # an string begin with '#' means an error
    else:
        tcp.send(enco(msg))
        ret = tcp.recv(BUFSIZ).decode() # return msg from server
        tcp.close() # close the connection
        return ret

