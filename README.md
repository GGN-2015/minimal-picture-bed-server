# minimal-picture-bed-server
一个极简的图床程序，python3 + HTTP 编写，此版本只支持命令行上传图片。

# 配置文件 config.py
根据自己的服务器以及端口设置``config.py``配置文件，语法如下：

```python
PORT = 10654          # 设置端口：请注意，如果端口已被占用，图床程序不能启动
HOST_IP = "127.0.0.1" # 如果你并不是在调试服务器，建议使用：HOST_IP = "auto"
```

# 启动 server.py
将 server.py 在前台/后台运行，在服务器上提供 server 服务。

# 上传图片 运行 upload.py
此版本只支持通过命令行上传图片到 server，并要求上传时 server.py 必须已在相应的服务器端口运行。

运行 upload.py 后只需要按照提示输入所需信息。

# 如何通过浏览器访问此图床

## 查看图片
http://HOST-IP:PORT/image/NAME

## 关闭服务器
http://HOST-IP:PORT/stop/

请注意：如果你不希望别人关闭自己的服务器，请修改代码删除此功能。
