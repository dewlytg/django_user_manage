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

