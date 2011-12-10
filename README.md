PyWapFeion  
==========

PyWapFetion是什么？能吃吗？  
==========

PyWapFetion是一个飞信的Python模块，使用Wap飞信协议。  
因为目前没有看到比较好的Python飞信模块（PyFetion虽然很强大，但是基于电脑客户端的协议，容易被各种验证码问题所困扰），所以自己动手写了一个。

怎么抱回家？
==========

在终端下输入（*nix）： `sudo pip install PyWapFetion` 或者 `sudo easy_install -U PyWapFetion`  
或者把源码下载下来，运行：`python setup.py install`

怎么玩？
==========
抱回家之后，直接在Python里import就可以。参考example.py  
如果没有抱回家，那么把PyWapFetion当前目录下再import.  

免费品尝有木有？
==========
GET或者POST数据到`http://lab-whtsky.rhcloud.com/fetion`  
数据：  
```python  
fid=手机号&password=密码&mobile=接受者手机号&msg=信息
```  
直接返回WAP飞信网页（实际使用中会返回True/False的bool,此处为了方便调试。）  
***  
比如：  
```python
from urllib import urlopen
print urlopen('http://lab-whtsky.rhcloud.com/fetion','fid=手机号&password=密码&mobile=接受者手机号&msg=信息').read()
```