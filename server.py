# i swear to use a single file to contain the whole server! -- GGN_2015
# GGN_2015 is a true programmer

version = "2020-08-16"
author  = "GGN_2015"

""" functions are listed as follows.
sloop(host, port) # open a server
getf(filename)    # read in all context in a file
"""

import socket
import os
import time
import traceback
import threading

cflag = True # important var to stop the server normally

from config import PORT    # read in config.py
from config import HOST_IP 

def matchpre(s, p):
    if type(s) == str:
        s += "#"
    else:
        s += b"#"
        p = p.encode("utf-8")

    for i in range(0, len(p)):
        if s[i] != p[i]:
            return False

    return True

def worker(inp):

    if matchpre(inp, "append|"): # get the message from console not explorer
        inp = inp[len("append|"):]
        lis = inp.split(b"|", 1)
        fname = lis[0] # filename
        res = lis[1]   # content of the file

        fi = open(fname, "ab") # write binary file
        fi.write(res)
        fi.close()

        return "[file-receiver] append file successfully. len = " + str(len(res))

    inp = inp.decode("utf-8")
    inp = inp.split("\n", 1)[0].replace("GET /", "").split(" HTTP")[0]
    #inp.replace("--", "..")  # if you want to show all the image/code in your server, uncomment this.

    if matchpre(inp, "image/"):
        print("[file-receiver] image instruction found.")

        inp = inp[len("image/"):]
        print("inp = " + inp)

        outp = "HTTP/1.1 200 OK\n"
        outp += "Accept-Ranges: bytes\n"
        outp += "Content-Type: image/png\n"
        outp += "Server: Apache-Coyote/1.1\n"
        outp += "Date: Fri, 21 Jul 2017 07:45:45 GMT\n"
        outp += "Content-Length: $SIZE$\n"
        outp += "Date: Fri, 21 Jul 2017 07:45:45 GMT\n\n"

        ans = b""
        try:
            print("[file-receiver] reading file...")
            fi = open(inp, "rb")
            ans = fi.read()
            fi.close()
            print("[file-receiver] reading file end...")
            outp.replace("$SIZE$", str(len(ans)))
        except:
            print("[file-receiver] error found...")
            outp = "HTTP/1.1 200 OK\nContent-Type: text"
            ans = traceback.format_exc().encode("utf-8")
            print(traceback.format_exc())
        outp = outp.encode("utf-8") + ans
        return outp # return bytes
        

    outp = """HTTP/1.1 200 OK\nContent-Type: html\nCharset: UTF-8\n\n"""
    outp += "<head><title>code</title><meta charset=\"utf-8\"></head>"
    outp += "<body>\n"

    # ----- add your code under this line -----


    if inp == "stop/" or inp == "stop":
        outp += "<h2>[file-receiver] server stop successfully</h2>"
        global cflag
        cflag = False

    elif matchpre(inp, "code/"):
        inp = inp[len("code/"):]
        outp += "<h2>"+inp+"</h2><hr>\n"
        outp += "<pre>"+getf(inp).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")+"</pre>"

    else:
        #outp += "[ggnserver] instruction not found."
        outp += "<h2>[file-receiver] you input:" + inp + "</h2>"

    outp += "</body>"

    # ----- add your code above this line -----

    return outp

conid = 0

def enco(s):
    if type(s) == str:
        return s.encode("utf-8")
    return s

def csend(cli, msg):
    while len(msg) > 500:
        cli.send(msg[:500])
        msg = msg[500:]
    cli.send(msg) # send a message divided

def consultant(cli): # use this in threads to answer for clients
    global conid
    conid += 1
    cid = conid # get an id by count

    try:
        print("[consultant] wait cli msg, cid = " + str(cid))
        msg = cli.recv(1024 * 1024 * 33)

    except:
        print("[consultant] error when wait cli msg. cid = " + str(cid))
        print(traceback.format_exc())

    print("[consultant] sending msg back cid = " + str(cid))
    csend(cli, enco(worker(msg)))
    cli.close()


def getf(filename): # read in all context in a file
    fi = open(filename, "r")
    ans = fi.read() # read all text in the file
    fi.close()
    return ans # return all the text in the file

def getip(): # get ip of the computer
    tcp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcp.connect(("8.8.8.8", 80))
    ip = tcp.getsockname()[0]
    tcp.close()
    return ip

def sloop(): # server loop
    global PORT
    global HOST_IP
    print("[file-reveiver] start.")
    print(" version : " + version + " author : " + author)
    print(" port: " + str(PORT))

    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if HOST_IP == "auto":
            HOST_IP = getip()

        tcp.bind((HOST_IP, PORT))
        tcp.listen(5)

    except:
        print("[file-receiver] can not create a server.")
        print(traceback.format_exc())
        tcp.close()
        return

    else:
        global cflag
        clfag = True # True means continue to loop

        while cflag: # cflag can be set by worker
            try:
                print("[file-receiver] waitting for connection ...")
                cli, addr = tcp.accept()

                th = threading.Thread(target = consultant, args = (cli, ))
                th.setDaemon(True)
                th.start()

            except:
                print("[file-receiver] error when solve consalt ...")
                print(traceback.format_exc())

        print("[file-receiver] tcp server end...")
        tcp.close()

if __name__ == "__main__":
    print("[file-receiver] it is going to start ...")
    sloop()
