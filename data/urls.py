from django.urls import path
from .views import *
#index,book,delete,pay,charge,search,download,test,category,register,contact,logn,conditions,upload,application

urlpatterns = [
    path('/about',about,name="about"),
    path('/apply',application,name='application'),
    path('/terms',conditions,name='terms'),
    path('/conditions',conditions,name='conditions'),
    path('/logout',logn,name='logout'),
    path('/contact',contact,name='contact'),
    path('/download',download,name='download'),
    path('/search',search,name='search'),
    path('/charge',charge,name='charge'),
    path('/pay',pay,name='pay'),
    path('',index,name='home'),
    path('/book',book,name='book'),
    path('/delete',delete,name='delete'),
    path('/test',test,name='test'),
    path('/cat',category,name='category'),
    path('/login',register,name='register'),
    path('/upload',upload,name='upload'),
    path('/private', work_thing,name="work"),
    ]