#!/usr/bin/python
# -*- encoding: utf-8 -*-

import time
import traceback
import sys

import translator
from server import getip

from config import WAN_IP
from config import PORT
#from image import sprint
#from image import cid

cid = ""
def sprint(s):
    global cid
    if type(s) == str:
        s = s.encode("utf-8")
    fi = open("tmp-out"+cid, "ab")
    fi.write(s)
    fi.close()

def print(s):
    sys.stderr.write(s+"\n")

def getf(filename): # 读取文本文件的全部内容
    fi = open(filename, "r")
    ans = fi.read()
    fi.close()
    return ans

try:

    #global cid
    cid = sys.argv[1]
    print("    [插件 image] cid = {" + cid + "}")

    inp = ""
    try:
        inp = input() # 获取输入信息
    except:
        pass # 不能获取说明没有输入信息

    sprint("HTTP/1.1 200 OK\nContent-Type: html\nCharset: UTF-8\n\n")

    sprint("<head>")
    #print("<title>欢迎页</title>")
    sprint("<meta charset=\"utf-8\">")
    sprint(getf("css.html"))
    sprint("<title>欢迎页</title>")
    sprint("</head>")

    sprint("<body style=\"max-width: 700px; margin: 0 auto\">")
    #print("<h1>" + time.ctime() + " </h1>")

    #if inp != "":
    #    print("<h4> 您的输入是{" + inp + "} </h4>")
    #    if inp[0] == "%":
    #        print("<h4> 解码后您的输入是{" + translator.translate(inp) + "}</h4>")

    sprint("<h1>欢迎使用 GGN_2015 的迷你图床程序</h1>")
    sprint("2020-11-15 Login this page from JLU's computer lab.<br><br>\n")
    sprint("2020-09-30 晓峰到此一游~\n")
    sprint("<table>")
    sprint("    <tr><th>公网 IP</th><th>局域网 IP</th><th>端口</th></tr>")
    sprint("    <tr><td>" + WAN_IP + "</td><td>" + getip() + "</td><td>" + str(PORT) + "</td></tr>")
    sprint("</table>")

    sprint("</body>")

    sprint("<p>来自 github 的开源 repository：<a onclick=\"window.location.href='https://github.com/GGN-2015/minimal-picture-bed-server/tree/full_plug_in'\">minimal-picture-bed-server/full_plug_in</a></p>")

    sprint("<p>GGN_2015 的 github 账户：<button onclick=\"window.location.href='https://github.com/GGN-2015'\">GGN_2015</button></p>")

    sprint("<h3>功能简介</h3>")

    sprint("<table>")
    sprint("    <tr><th>功能</th><th>链接/介绍</th></tr>")
    sprint("    <tr><td>显示文件列表</td><td><button onclick=\"window.location.href='http://" + WAN_IP + ":" + str(PORT) + "/list/'\">list</button></td></tr>")
    sprint("    <tr><td>图床语法</td><td>http://HOST-IP:PORT/image/NAME</td></tr>")
    sprint("</table>")

    sprint("<h2>一些 GGN_2015 开发的智障功能</h2>")
    sprint("<button onclick=\"window.location.href='/matrix-mul'\">三阶矩乘(手机)</button>")
    sprint("<button onclick=\"window.location.href='/bbs'\">极简论坛(电脑)</button>")
    sprint("<button onclick=\"window.location.href='/2048'\">2048(都行)</button>")

except:
    sprint("<hr>")
    sprint("<h1>执行程序时出错!</h1>")
    sprint("<img src=\"http://" + WAN_IP + ":" + str(PORT) + "/image/cry.jpg\" style=\"width:20%\"></img><br><br>")
    sprint("<pre>" + traceback.format_exc().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")) # 输出错误信息
    sprint("</pre></body>")
