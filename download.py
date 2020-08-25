#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import os
import time
import traceback

import translator
from server import getip

from config import WAN_IP
from config import PORT
import ggntalk

def eprint(s):
    sys.stderr.write(s+"\n")

cid = ""

def sprint(s):
    if type(s) == str:
        s = s.encode("utf-8")
    fi = open("tmp-out" + cid, "ab")
    fi.write(s+b"\n")
    fi.close

def getf(filename): # 读取文本文件的全部内容
    fi = open(filename, "r")
    ans = fi.read()
    fi.close()
    return ans

try:
    #global cid
    cid = sys.argv[1]

    inp = ""
    try:
        inp=input()
    except:
        pass

    fname = inp

    if not os.path.isfile(fname): # 文件不存在
        
        outp = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
        outp += "<head><meta charset=\"utf-8\"><title>404 Not Found</title></head>"
        outp += "<body style='max-width: 500px; margin: 0 auto'><h4>喵呜~ 您要下载的文件不存在!</h4>"
        outp += "<img src=\"http://" + WAN_IP + ":" + str(PORT) + "/image/cry.jpg\"></img></body>"
        
        sprint(outp)
        os._exit(0)

    outp = "HTTP/1.1 200 OK\n"
    outp += "Accept-Ranges: bytes\n"
    outp += "Content-Type: application/octet-stream\n"
    outp += "Server: Apache-Coyote/1.1\n"
    outp += "Date: " + time.ctime() + " GMT\n"
    outp += "Content-Length: $SIZE$\n\n"

    fi = open(fname, "rb")
    ans = fi.read()
    outp.replace("$SIZE$", str(len(ans)))
    fi.close()

    sprint(outp.encode("utf-8") + ans)
except:
    sprint("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")
    sprint("<head><meta charset=\"utf-8\"><title>404 Not Found</title></head>")
    sprint("<body style='max-width: 500px; margin: 0 auto'>")
    sprint("<h1>执行程序时出错!</h1>")
    sprint("    <img src=\"http://" + WAN_IP + ":" + str(PORT) + "/image/cry.jpg\" style=\"width:20%\"></img><br><br>")
    sprint("    <pre>" + traceback.format_exc().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")) # 输出错误信息
    sprint("    </pre>\n</body>")
