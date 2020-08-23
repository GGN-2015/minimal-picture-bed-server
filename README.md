# minimal-picture-bed-server
一个极简的图床程序，python3 + HTTP 编写，此版本只支持命令行上传图片。

# 配置文件 config.py
根据自己的服务器以及端口设置``config.py``配置文件，语法如下：

```python
# -*- 这是 config.py 文件的内容解释 -*-
PORT = 10654          # 设置端口：请注意，如果端口已被占用，图床程序不能启动
HOST_IP = "127.0.0.1" # 建议使用：HOST_IP = "auto"， 否则这一条需要设置成您的服务器在局域网中的 IP
WAN_IP = "127.0.0.1"  # 这一条需要手动设置成您的服务器在广域网上的 IP
```

# 启动 server.py
将 server.py 在前台/后台运行，在服务器上提供 server 服务。

1. ``nohup python3 server.py`` 无显示运行 server
2. ``Ctrl-Z`` 将该程序挂起
3. ``jobs`` 命令查看该挂起进程的job编号
4. ``bg %job编号`` 将该程序在后台运行
5. ``disown %job编号`` 将该进程与当前控制台脱离联系

# 上传图片 运行 upload.py
此版本只支持通过命令行上传图片到 server，并要求上传时 server.py 必须已在相应的服务器端口运行。

运行 upload.py 后只需要按照提示输入所需信息。

一定要注意：重名文件并不会被覆盖，而会被“连接”，即第二个文件追加到第一个文件尾部。

# 如何通过浏览器访问此图床

## 查看图片
``http://HOST-IP:PORT/image/NAME.jpg`` (or NAME.png)

## 查看 HTML 文件
``http://HOST-IP:PORT/show/NAME.html``

## 查看源代码
``http://HOST-IP:PORT/code/NAME`` (含后缀名)

## 运行一个 python 程序并将程序的输出作为 HTML 代码传回浏览器

``http://HOST-IP:PORT/run/NAME`` (不含后缀名".py")

## 访问图标文件
``http://HOST-IP:PORT/favicon.ico``
(如果图标不对，你可以先访问这个网址，此后浏览器会储存这个正确的图标)

# 如何关闭服务器

1. 执行命令： ps -ef | grep python
2. 在列表中找到进程 "python3 server.py" 对应的编号
3. 执行命令： kill -9 <进程编号> 杀死进程

