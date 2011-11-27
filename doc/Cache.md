PyWapFetion：缓存
=================

概述
====
PyWapFetion是基于WapFetion的飞信SDK，WapFetion中的信息发送操作需要接收方的飞信ID.  
取得飞信ID的方法是执行搜索->正则表达式取唯一的ID值。  
但这样有些问题：  
***

* 正则表达式毕竟有时间消耗  
* 网络操作更有时间消耗  
* 最恐怖的是，移动的服务器还不稳定，经常会出现访问错误  

***
所以，我们需要缓存来提高速度和稳定性。  

结构
====
    class Cache:  
        def __init__(self,path)  
        def get(self,phone)  
        def put(self,phone,id)  
        def rm(self,phone)  
        def save(self)  
        def exit(self)  
       
使用
====    
    from PyWapFetion import Cache  
    cache = Cache(path = 'filename')  
path：缓存文件路径。可以是相对路径，也可以是绝对路径。  
在创建Fetion类时默认开启缓存，缓存的默认文件名为`Fetion.cache`    
Cache把手机号与飞信号存入字典，在初始化时从文件读入字典（没有则新建），在调用`save()`时将字典保存到文件。  
1. get():从缓存中读取数据  
示例：`get('手机号')`。如果存在本数据返回飞信号，否则返回False  
2.put():将数据写入缓存  
示例：`put('手机号','飞信号')`。写入成功返回True，否则返回False  
3.rm():从缓存中删除数据  
示例：`rm('飞信号')`。删除成功返回True，否则返回False  
4.save()：保存缓存到文件  
示例：`save()`。  
5.exit()：退出缓存
示例：`exit()`。会自动保存数据并删除变量。


注意
====
* Cache类使用Python内置的marshal模块进行持久化储存，marshal模块**不能保证各版本间的兼容性**。如果你要更换Python版本，请手动删除缓存文件（默认名为`Fetion.cache`）。  
* 因为Cache是在调用`save()`时才保存文件到更改，请保证**每一个Cache实例独享一个缓存文件**  