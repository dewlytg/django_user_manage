from django.db import models

# Create your models here.
class classes(models.Model):
    caption = models.CharField(max_length=32)


class student(models.Model):
    username = models.CharField(max_length=32)
    cls = models.ForeignKey("classes",on_delete=models.CASCADE)


class teacher(models.Model):
    username = models.CharField(max_length=32)
    cls = models.ManyToManyField("classes")


class administrator(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)


class Book(models.Model):
    name = models.CharField(max_length=64)
    publish = models.ForeignKey("Publisher",on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=64)
    m = models.ManyToManyField("Book")

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Upload(models.Model):
    path = models.CharField(max_length=128)



class User(models.Model):
    username = models.CharField(max_length=32,unique=True)
    email = models.EmailField(max_length=32,unique=True)
    pwd = models.CharField(max_length=128)
    ctime = models.DateTimeField(auto_now_add=True)
    user_type = models.ForeignKey(to="UserType",on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    def save(self,*args,**kwargs):
        self.pwd = hashlib.md5(self.pwd.encode()).hexdigest()
        super(User,self).save(*args,**kwargs)


class UserType(models.Model):
    caption = models.CharField(max_length=16,unique=True)
    menus = models.ManyToManyField("Menu")

    def __str__(self):
        return self.caption


class Menu(models.Model):
    name = models.CharField(max_length=32,unique=True)

    def __str__(self):
        return self.name


class Option(models.Model):
    name = models.CharField(max_length=32,unique=True)
    url_path = models.CharField(max_length=64,unique=True)
    menu = models.ForeignKey("Menu",on_delete=models.CASCADE,related_name="op")

    def __str__(self):
        return self.name

