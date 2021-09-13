"""Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from data.views import contact
from django.contrib import admin
from django.urls import path,include
from data import urls,views
from rest_framework import routers
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from django.http import HttpResponse
from django.views.static import serve

handler404 = 'data.views.handler404'
handler500 = 'data.views.handler404'

router      = routers.DefaultRouter()
router.register(r'users',views.UserViewset)
router.register(r'groups',views.GroupViewset)

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    url('^about',views.about,name='about'),
    url('^login',views.register,name='login'),
    url('^apply',views.application,name='application'),
    url('^contact',contact,name='contact'),
    url('^$',include(urls)),
    url('^',include(router.urls)),
    url('amin/',include('rest_framework.urls',namespace='rest_framework'), name="users"),
    path('master/', admin.site.urls),
    path('data',include(urls)),
    url('^private', views.work_thing,name="workthing"),
    url(r'^robots.txt', lambda x: HttpResponse("User-Agent: *\nDisallow:", content_type="text/plain"), name="robots_file"),
]

# y   = 1
# if y==1:
#     urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# else:
#     urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
