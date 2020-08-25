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

# 上传文件

``scp <path> <usr>@<HOST-IP>:<new-path>`` 取缔了用 upload.py 上传文件的方式。

# 更换 logo

将你的 png 格式的 logo 上传到 server.py 所在的文件夹，将其命名为 favicon.png 即可。

# 如何通过浏览器访问此图床

万物皆插件: image, code, welcome, list, facicon.ico 是五个自带的插件。

插件独立于 server.py 之外，各自占据一个 .py 文件。

## 查看图片
``http://HOST-IP:PORT/image/NAME.jpg`` (or NAME.png)

## 查看源代码
``http://HOST-IP:PORT/code/NAME`` (NAME 含后缀名)

## 运行一个 python 程序并将程序的输出作为 HTML 代码传回浏览器

``http://HOST-IP:PORT/NAME`` (不含后缀名".py")

## 访问图标文件
``http://HOST-IP:PORT/favicon.ico``
(如果图标不对，你可以先访问这个网址，此后浏览器会储存这个正确的图标)

## 显示所有文件
``http://HOST-IP:PORT/list/`` 请注意不要省略最右侧的"/"

## 下载一个文件
``http://HOST-IP:PORT/download/NAME`` (含后缀名)

## 访问欢迎页
``http://HOST-IP:PORT/`` 或
``http://HOST-IP:PORT/welcome`` (两者等价)

# 如何关闭服务器

1. 执行命令： ps -ef | grep python
2. 在列表中找到进程 "python3 server.py" 对应的编号
3. 执行命令： kill -9 <进程编号> 杀死进程

程序结束后端口可能不会立刻解除占用，如果希望端口立刻解除占用，请重启服务器。

