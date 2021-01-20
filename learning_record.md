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
   
4. 登陆的时候可能会出现如下错误：

   * ![image-20210117220104314](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20210117220104314.png)

   * 返回去看登录模板

     * ```html
       <form action="{% url 'examapp:login' %}" method="post">
           {% csrf_token %}
           <div class="login-field">
               <input type="text" name="" required=""/>
               <label>Username</label>
           </div>
           <div class="login-field">
               <input type="password" name="" required=""/>
               <label>Password</label>
           </div>
           <button type="submit">Submit</button>
       </form>
       ```

   * 应该修改为

     * ```html
       <form action="{% url 'examapp:login' %}" method="post">
           {% csrf_token %}
           <div class="login-field">
               <input type="text" name="username" required=""/>
               <label>Username</label>
           </div>
           <div class="login-field">
               <input type="password" name="password" required=""/>
               <label>Password</label>
           </div>
           <button type="submit">Submit</button>
       </form>
       ```

5. 在学生进入考试界面的时候，出现了这样的问题，`exam.html`拿不到paper的信息。

   * 向`exam.html`传递paper的信息方式如下：

     * ```python
       paper = models.Paper.objects.filter(id=paper_id)  # 这样得不到
           if paper.exists():
               print('count:', paper.count())
       
           # 确保学生唯一的一张考试试题
           # paper    = get_object_or_404(models.Paper, id=paper_id)
       
           context = {
               'student': student,
               'paper': paper,
               'subject': subject,
           }
       
           return render(request, 'exam.html', context)
       ```

   * 但是界面上却没有

     * ![image-20210119003054317](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20210119003054317.png)

   * 最后才发现问题是`paper = models.Paper.objects.filter(id=paper_id)`，这是一个集合，但我在`exam.html`中却直接用的是paper，把它当作元素用了。

   * ```html
     {% for choice in paper.choice_q.all %}
     ```

   * 所以要么在`exam.html`中遍历集合，要么采用`paper    = get_object_or_404(models.Paper, id=paper_id)`，我选择了后者，因为答题者一次只能答一份试卷。

   



