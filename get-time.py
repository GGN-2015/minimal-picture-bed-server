import time
import traceback

inp = ""
try:
    inp = input() # 获取输入信息
except:
    pass # 不能获取说明没有输入信息

print("<head>")
print("<title>获取系统时间</title>")
print("<meta charset=\"utf-8\">")
print("</head>")

print("<body>")
print("<h1> 当前的时间是 " + time.ctime() + " </h1>")
if inp != "":
    print("<h1> 您的输入是" + inp + " </h2>")
print("</body>")
