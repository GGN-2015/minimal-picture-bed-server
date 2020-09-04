#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import os
import time
import traceback

import translator
from server import getip
from server import matchpre

from config import WAN_IP
from config import PORT
import ggntalk

def print(s):
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
    global cid
    cid = sys.argv[1]

    inp = ""
    try:
        inp=input()
    except:
        pass

    os.system("ls > list.out") # for linux only
    
    outp = """HTTP/1.1 200 OK\nContent-Type: html\ncharset: UTF-8\n\n"""
    outp += "<head><title>显示目录</title><meta charset=\"utf-8\">"
    outp += getf("css.html")
    outp += "</head><body style=\"max-width: 1000px; margin: 0 auto\">\n"

    nlis = getf("list.out").split("\n")
    
    outp += "<h1>list</h1>\n"

    outp += "<table>\n"
    if inp == "":
        outp += "    <tr><td>筛选方式</td><td><a style=\"color: red\" onclick=\"window.location.href='http://"+WAN_IP+":"+str(PORT)+"/list/'\">不筛选</a></td><td><a onclick=\"window.location.href='http://"+WAN_IP+":"+str(PORT)+"/list/image/'\">仅图片</a></td><td><a onclick=\"window.location.href='http://"+WAN_IP+":"+str(PORT)+"/list/code/'\">仅代码</a></td></tr>"
    elif matchpre(inp, "image/"):
        outp += "    <tr><td>筛选方式</td><td><a onclick=\"window.location.href='http://"+WAN_IP+":"+str(PORT)+"/list/'\">不筛选</a></td><td><a style=\"color: red\" onclick=\"window.location.href='http://"+WAN_IP+":"+str(PORT)+"/list/image/'\">仅图片</a></td><td><a onclick=\"window.location.href='http://"+WAN_IP+":"+str(PORT)+"/list/code/'\">仅代码</a></td></tr>"
    elif matchpre(inp, "code/"):
        outp += "    <tr><td>筛选方式</td><td><a onclick=\"window.location.href='http://"+WAN_IP+":"+str(PORT)+"/list/'\">不筛选</a></td><td><a onclick=\"window.location.href='http://"+WAN_IP+":"+str(PORT)+"/list/image/'\">仅图片</a></td><td><a style=\"color: red\" onclick=\"window.location.href='http://"+WAN_IP+":"+str(PORT)+"/list/code/'\">仅代码</a></td></tr>"
    else:
        outp += "    <tr><td>筛选方式</td><td><a onclick=\"window.location.href='http://"+WAN_IP+":"+str(PORT)+"/list/'\">不筛选</a></td><td><a onclick=\"window.location.href='http://"+WAN_IP+":"+str(PORT)+"/list/image/'\">仅图片</a></td><td><a onclick=\"window.location.href='http://"+WAN_IP+":"+str(PORT)+"/list/code/'\">仅代码</a></td></tr>"

    outp += "</table>\n"

    outp += "<table border=\"2\">\n"
    outp += "<tr>\n<th>目录列表</th>\n<th>是否可下载</th>\n<th>下载键</th><th>缩略图</th></tr>\n"

    for x in nlis:
        if x == "" or x == "list.out" or x.find("tmp-in") != -1:
            continue
        if os.path.isfile(x):

            flis = x.split(".")
            appendix = flis[-1] # 最后一个元素是后缀名
            
            if matchpre(inp, "code/") and not( appendix in ["py", "html"]):
                continue

            if matchpre(inp, "image/") and not( appendix in ["png", "jpg"]):
                continue
            
            outp += "<tr>\n<td>" + x + "</td>\n"
            outp += "<td>是</td>\n"
            if appendix in ["py", "html"]:
                outp += "<td><button onclick=\"window.location.href='http://" + WAN_IP + ":" + str(PORT) + "/download/" + x + "'\">下载</button> <button onclick=\"window.location.href='http://"+WAN_IP+":"+str(PORT)+"/code/"+x+"'\">预览代码</button></td><td><img style=\"width: 20px\" src=\"http://"+WAN_IP+":"+str(PORT)+"/image/code.jpg\"></img></td>\n"
            elif appendix in ["png", "jpg"]:
                outp += "<td><button onclick=\"window.location.href='http://" + WAN_IP + ":" + str(PORT) + "/download/" + x + "'\">下载</button> <button onclick=\"window.location.href='http://" + WAN_IP + ":" + str(PORT) + "/image/" + x + "'\">预览图片</button></td><td><img style=\"width: 20px\" src=\"http://"+WAN_IP+":"+str(PORT)+"/image/"+x+"\"></img></td>\n"
            else:
                outp += "<td><button onclick=\"window.location.href='http://" + WAN_IP + ":" + str(PORT) + "/download/" + x + "'\">下载</button></td><td><img style=\"width: 20px\" src=\"http://"+WAN_IP+":"+str(PORT)+"/image/text.jpg\"></img></td>"
        else: # 文件夹
            if matchpre(inp, "code/") or matchpre(inp, "image/"):
                continue
            
            outp += "<tr>\n<td>" + x + "</td>\n"    
            outp += "<td>否</td>\n"
            outp += "<td>禁用</td><td><img style=\"width: 20px\" src=\"http://"+WAN_IP+":"+str(PORT)+"/image/folder.jpg\"></img></td>\n"
        outp += "</tr>\n"
        print("    [服务器 工人] [文件列表]" + x)
    
    outp += "</table>"
    outp += "</body>"

    os.system("rm list.out")
    sprint(outp)
    os._exit(0)

except:
    sprint("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")
    sprint("<head><meta charset=\"utf-8\"><title>404 Not Found</title></head>")
    sprint("<body style='max-width: 500px; margin: 0 auto'>")
    sprint("<h1>执行程序时出错!</h1>")
    sprint("    <img src=\"http://" + WAN_IP + ":" + str(PORT) + "/image/cry.jpg\" style=\"width:20%\"></img><br><br>")
    sprint("    <pre>" + traceback.format_exc().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")) # 输出错误信息
    sprint("    </pre>\n</body>")
