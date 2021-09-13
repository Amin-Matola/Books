from django.db import models
from django.contrib.auth.models import User

#----------------------------------------------------------------
# ...................Create your models here.....................|
#----------------------------------------------------------------

class Users(models.Model):
        user                = models.ForeignKey(User,on_delete=models.CASCADE)
        mobile              = models.IntegerField(null=False)
        gender              = models.CharField(max_length=7)
        address             = models.TextField(max_length=150)
        paid                = models.BooleanField(default=False)
        downloads           = models.IntegerField(default=0)

class Book(models.Model):
        book_title          = models.CharField(max_length=100,null=False)
        auther              = models.CharField(max_length=60)
        date_published      = models.DateTimeField(auto_now_add=True)
        book_image          = models.FileField()
        borrowed            = models.BooleanField(default=False)
        category            = models.CharField(max_length=50,null=False)
        downloads           = models.IntegerField(null=False,default=0)

class Download(models.Model):
        downloader          = models.ForeignKey(User,on_delete=models.CASCADE)
        book                = models.ForeignKey(Book,null=False,on_delete=models.CASCADE)
        download_date       = models.DateTimeField(auto_now_add=True)


class Vistor(models.Model):
        user                = models.ForeignKey(User,on_delete=models.CASCADE)
        computer_name       = models.CharField(max_length=100)
        computer_ip         = models.TextField()
        last_visted         = models.DateTimeField(auto_now_add=True)
