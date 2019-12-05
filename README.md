# NJUPT_Autojudge

:heart:使用了高亮学长给力的[NJUPT的API](https://github.com/gaoliang/NJUPT-API),获得COOKIE后使用selenium登录



#### 安装依赖库

```
$ pip3 install -r requirements.txt
```

#### 如何使用

```
$ python elvaluate.py
```



#### 如何设置?

将账号密码在`dada.conf`中设置,其中`Chromedriver`的位置也在其中设置

```
[account]
B17050322 = ...

[config]
webdriver = C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe
```


#### 5.22反馈更新
大一时写的时候,课程内容的两个下拉列表是一样的,所以没注意。导致了这次使用时，非主课，如认识实习，及重修课无法自动测评。
5.25蓝桥杯国赛结束后希望有时间能把这坑补上。
最近看了下POST请求，发现其实直接模拟表单也是挺容易的。之后有时间再弄了。

#### 12.5更新
用Selenium模拟点击的代码放弃维护了，重新写了一份模拟请求的代码，完成速度更快，请君使用[Njupt_AutoJudge_requests](https://github.com/Freedomisgood/Njupt_AutoJudge_requests):smile:
