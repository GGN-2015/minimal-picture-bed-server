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
    
    if not os.path.isfile(inp):
        
        outp = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
        outp += "<head><meta charset=\"utf-8\"><title>404 Not Found</title></head>"
        outp += "<body style='max-width: 500px; margin: 0 auto'><h4>喵呜~ 您的代码丢了!</h4>"
        outp += "<img src=\"http://" + WAN_IP + ":" + str(PORT) + "/image/cry.jpg\"></img></body>"
        
        sprint(outp)
        os._exit(0)

    
    outp = """HTTP/1.1 200 OK\nContent-Type: html\nCharset: UTF-8\n\n"""
    outp += "<head><title>显示代码</title><meta charset=\"utf-8\">"
    outp += getf("css.html")
    outp += "</head>\n<body style=\"max-width: 700px; margin: 0 auto\">\n"

    outp += "    <h1>"+inp+"</h1>\n"
    outp += "    <pre>"+getf(inp).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")+"</pre>\n"
    outp += "    <img src=\"http://" + WAN_IP + ":" + str(PORT) +"/image/look.png\"></img>\n"
    outp += "</body>\n"

    sprint(outp)

except:
    sprint("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")
    sprint("<head><meta charset=\"utf-8\"><title>404 Not Found</title></head>")
    sprint("<body style='max-width: 500px; margin: 0 auto'>")
    sprint("<h1>执行程序时出错!</h1>")
    sprint("    <img src=\"http://" + WAN_IP + ":" + str(PORT) + "/image/cry.jpg\" style=\"width:20%\"></img><br><br>")
    sprint("    <pre>" + traceback.format_exc().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")) # 输出错误信息
    sprint("    </pre>\n</body>")
