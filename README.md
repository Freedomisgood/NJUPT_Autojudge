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