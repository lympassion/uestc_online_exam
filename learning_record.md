### django 学习记录

***

**写在前面**：寒假里因为要用python做一个自动组卷系统。之前也因为小组合作用过django，但是那个时候不系统，所以借此机会更深入地理解一个系统的建立过程。







#### 1. [django文档](https://docs.djangoproject.com/en/3.0/intro/)

**django的设计模式是MTV，外加url分离器。**

1.1 M(model)，模式，本质上是一个数据库布局，同时还包括其他的元数据。负责业务对象和数据库的映射。[关于models的介绍](https://docs.djangoproject.com/en/3.0/topics/db/models/)

* ![image-20210114133104502](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20210114133104502.png)

1.2 T(templates)，模板，就是HTML，展示信息。

1.3 V(views)，视图，负责业务逻辑，供url分离器调用，它本身会调用model和templates。

* ![image-20210114141312939](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20210114141312939.png)

**有关数据库的操作**

1.4 [访问对象以及api](https://docs.djangoproject.com/en/3.0/intro/tutorial02/#introducing-the-django-admin)



#### 2. 相关参考说明

2.1 [登录参考](https://blog.csdn.net/qq_41325698/article/details/102591169)





#### 疑惑及解答

1. HttpRequest对象如何发出？
   
   * [Django中的Request](https://blog.csdn.net/u014745194/article/details/73850614)
   
2. 请求对象何时应该为POST？
   * [GET and POST](https://docs.djangoproject.com/en/3.1/topics/forms/)
   * [Write a minimal form 中的简单解释](https://docs.djangoproject.com/en/3.1/intro/tutorial04/#write-a-minimal-form)
   
3. `django.core.exceptions.ImproperlyConfigured: AUTH_USER_MODEL refers to model 'exmpapp.User' that has not been installed`

   * 这个问题是当我把学生和老师都当作User时，在`settings.py`中加入`AUTH_USER_MODEL = "exmpapp.User"`出现的。

   * 网上所有的解决方法都翻了一遍，再重新搜索问题时，所有的链接都这样

     * ![image-20210116231346500](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20210116231346500.png)

   * 后来再在`settings.py`中盯

     * ```python
       # This way we are telling Django to use our custom model instead the default one.
       # AUTH_USER_MODEL = "exmpapp.User"
       AUTH_USER_MODEL = "examapp.User"
       ```

     * ……



