# Python-Django天天生鲜项目（dailyfresh）
此项目是学习python的django框架时参考某python教程的项目所完成的实践，<br>
主要功能：用户注册、用户登录、用户中心、商品列表、商品详情、图片上传、购买商品、订单的生成、支付、评价等。
### 技术选型
Python + Django框架 + MySQL + Redis + Celery + FastDFS + Nginx
### 详细（模块）设计
>用户模块
>>注册账户<br>
激活账户<br>
登录<br>
个人信息中心<br>
收货地址<br>
退出登录<br>

>商品模块
>>首页<br>
商品检索<br>
商品列表<br>
商品详情<br>

>购物车模块
>>添加商品<br>
移除商品<br>
修改购物车中商品数量<br>

>订单模块
>>确认订单<br>
生成订单<br>
支付订单（支付宝）<br>
评价订单<br>
