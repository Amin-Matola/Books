from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Users,Book,Download
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User,Group
from .serializers import UserSerializer,GroupSerializer
from rest_framework import viewsets
from django.conf import settings
import os
import stripe
from django.core.files.storage import default_storage
#from django.core.servers.basehttp import FileWrapper
import mimetypes
from urllib import request as req
import requests as rt
from datetime import datetime

class UserViewset(viewsets.ModelViewSet):
    """An API for editing Users"""
    queryset        = User.objects.all().order_by('-date_joined')
    serializer_class   = UserSerializer

class GroupViewset(viewsets.ModelViewSet):
    """An API for editing groups """
    queryset        = Group.objects.all()
    serializer_class= GroupSerializer


"""
............... Adding Views ...................

"""

def handler404(request):
    """ If pge can't be found, or internal error occurs """
    return render(request,"404.html",{'url':request.path})

def about(request):
    """ Return the side description/about information """
    return render(request,'data/about.html',{})

def contact(request):
    """ Contact form """
    if request.method == 'GET':
        return render(request,"data/contact.html",{})

    sender      = request.POST.get('email','')
    message     = request.POST.get('message','')
    phone       = request.POST.get('phone','')

    if not sender.__contains__("@") or not len(message.strip()):
         return render(request,"data/contact.html",{"error":True})

    rq          = rt.post('https://script.google.com/macros/s/AKfycbzjJIf2niIw0BBt-uZUgeSkdUcOVKWvxLCprBA_iZsMUItwkeg/exec',
    data        = {'email':sender,'message':message,'phone':phone})
    if rq.status_code == 200:
        return render(request,"data/contact.html",{'success':True})
    return render(request,"data/contact.html",{})

#-------------------------
# Applications
#-------------------------------
def application(request):
    if request.method=='GET':
        return render(request,'data/application.html',{})
    to      = request.POST.get('to', '')
    subject = request.POST.get('subject', '')
    typ     = request.POST.get('type', '')

    rq      = rt.post('https://script.google.com/macros/s/AKfycbxSGD8JSEbvymnhDXq4g1qiUBjAudPxXcY5-cSB_PB-dXPA0asc/exec',
    data    = {'email':to,'type':typ, 'title':subject})
    if rq.status_code == 200:
        #return HttpResponse(subject)
        return render(request,'data/application.html', {'success':True})
    return render(request, 'data/application.html', {})

#---------------------------
# The usage conditions
#---------------------------
def conditions(request):
    """ Return terms and conditions of this site """
    return render(request,'data/conditions.html',{})


def logn(req):
    """ Login and authenticate users """
    email           = req.POST.get('email','')
    password        = req.POST.get('password','')
    userv           = False
    user            = False
    if req.GET.get('out', ''):
       logout(req)
       return redirect('register')
    
    if email.__contains__("@"):
        try:
            user        = User.objects.get(email=email)
            userv       = user.check_password(password)
        except:
            pass
    else:
        user            = authenticate(username = email,password=password)
    if user or userv:
        login(req, user)
        books           = Book.objects.all().order_by('pk')[:6]
        return render(req, 'data/books.html', {'buks':books,'current_user':user})

    return render(req,'data/people.html', {'login':True, 'error':True, 'u':email})


def load_user(class_name, email):
    try:
        user            = class_name.objects.get(email = email)
        return user
    except Exception as e:
        return False


def index(request):
    """ Returning available books from home"""
    books            = Book.objects.all().order_by('pk')[:6]
    return render(request, 'data/books.html', {'buks':books, 'current_user':request.user})

def register(request):
    """ Register users """
    if request.method == 'GET':
        if request.GET.get('login',''):
            return render(request, 'data/people.html', {'login':False})
        return render(request, 'data/people.html', {'login':True})
    if request.GET.get('register',''):
        return logn(request)
    try:
        username        = request.POST.get('username','')
        fname           = request.POST.get('fname',"")
        lname           = request.POST.get('lname',"")
        mobile          = request.POST.get('mobile','')
        email           = request.POST.get('email','')
        gender          = request.POST.get('gender',"")
        address         = request.POST.get('address','')
        role            = request.POST.get('role','')
        password        = request.POST.get('password','')
    except Exception as e:
        return HttpResponse("<h2>Hello %s, please fill your form correctly............"%request.POST.get('fname',''))

    if load_user(User, email):
        return HttpResponse("<h2>You are already registered, please <a href='/login'>login</a></h2>")
    else:
        logging_user    = User(username=username,first_name=fname,last_name=lname,email=email,password=password)
        logging_user.set_password(password)
        logging_user.save()

    if gender:
        gender= 'male'
    else:
        gender= 'female'

    user    = Users(
    user=logging_user,
    mobile=mobile,
    gender=gender,
    address=address)


    try:
        user.save()
    except Exception as e:
        return HttpResponse("<h2>Oops Oops, that is an error</h2><hr> %s"%e)
    return redirect('/')


def category(request):
    """ Get books in accordance to the category """
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('/login')
        cat     = request.GET.get('cat','')
        buks    = Book.objects.filter(category=cat).all()
        user    = request.user

        return render(request,'data/category.html',{'buks':buks,'current_user':user})

    return HttpResponse("Method not allowed")

def book(request):
    """ Get all available books according to the search"""
    buks        = Book.objects.all()[:5]
    people      = Users.objects.all()
    user        = request.user
    if request.method=='GET':
        if not request.user.is_authenticated:
            return register(request)
        if request.GET.get('cat',''):
            sub     = request.GET.get('sub','')
            cat     = request.GET.get('cat','')
            buks    = Book.objects.filter(category=cat).all()[:5]
            if sub:
                buks    = Book.objects.filter(category=cat) .filter(book_title__contains=sub.title()).all()
            try:
                return render(request,'data/%s.html'%cat,{'buks':buks,'current_user':user})
            except:
                return render(request,'data/books.html',{'buks':buks,'current_user':user})
        elif request.GET.get('borrowed',''):
            try:
                return render(request,'data/borrowed.html',{'buks':buks,'current_user':user})
            except Exception as e:
                return HttpResponse("<h1>Oops! Oops! That is an error</h1><hr>%s"%e)
        elif request.GET.get('people',''):
            return render(request,'data/people.html',{'people':people,'current_user':user})
        else:
            return render(request,'data/books.html',{'buks':buks,'current_user':user})

    if not request.user.is_authenticated:
        return register(request)

    title       = request.POST['title'].title()
    auther      = request.POST.get('auther','')
    image       = request.FILES.get('image','')
    date        = request.POST.get('date','')
    category    = request.POST.get('category','')

    if image:
        #if request.user.is_superuser:
            path    = os.path.join(settings.MEDIA_ROOT,image.name)
            #image  = req.urlretrieve(url, path)
            savedto = default_storage.save(path, image)
        # else:
        #     image = req.urlretrieve('http://coders.pythonanywhere.com/media/net.jpg',image.name)

    #book           = Books(book_title=title,auther=auther,book_image=path)
    documents       = ['pdf','docx']
    file_type       = image.name.split('.')[-1]
    #if file_type in documents:
    #    book       = Book(book_title=title,auther=auther,book_image='https://amix.pythonanywhere.com/static/icon.jpg' ,date_published=date,category=category)
    #else:
    book            = Book(book_title=title,auther=auther,book_image=image.name,date_published=date,category=category)
    book.save()
    try:
        return render(request,'data/books.html',{'book':True,'current_user':user,'buks':buks})
    except Exception as e:
        return render(request,'uploads/librarian.html',{'error':True})

def delete(request):
    """ 
        Delete book from the frontend, 
        only admin can see this button 
    """
    b_id    = request.GET.get('book','')
    
    if b_id and request.user.is_superuser:
        bookToDelete    = Book.objects.get( id = int(b_id) )

        try:
            bookToDelete.delete()
            return redirect('/data')
        except Exception as e:
            return HttpResponse("<h1>Oops! Oops! That is an error:</h1><hr>%s"%e)
    return HttpResponse("<h1>No book selected</h1>")

#----------------------------payments---------------------------------------#
def pay(request):
    return render(request, 'data/payments.html', {'key':settings.STRIPE_PUBLISHABLE_KEY})

def charge(request):
    """ Manage Payments, uing stripe """
    if request.method == 'POST':
        stripe.api_key  = settings.STRIPE_SECRET_KEY
        charge          = stripe.Charge.create(
                            amount=500,
                            currency='usd',
                            description='A Django charge',
                            source=request.POST['stripeToken']
                        )
        fuser           = User.objects.get(pk=request.user.pk)
        user            = Users.objects.get(user=fuser)
        user.paid       = True
        user.save()
        errortype       = 'Hello %s, Thanks for upgrading... Now you are our member. you can get books as much as you want!'%fuser.username
        return render( request,'data/books.html', {'buks':Book.objects.all()[:5], 'errortype':errortype})
    else:
        return render(request, 'data/payments.html',{})

def search(request):
    if request.method == 'GET':
        user        = request.user
        data        = request.GET.get('q','')
        try:

            book    = Book.objects.filter(book_title__contains=data.title()).all()
        except Exception as e:
            return HttpResponse("That was an error :<hr>!%s"%e)
    return render(request,'data/books.html',{'search':book,'current_user':user,'total':len(book)})

def download(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('register')
        ruser  = User.objects.get(pk=request.user.pk)
        user   = Users.objects.get(user=ruser)
        if not user.paid:
            if user.downloads>=5:

                return render(request,'data/books.html', {'buks':Book.objects.all()[:5], 'etype':True})

        f               = request.GET.get('img','')

        book            = Book.objects.get(pk=f)
        f_file          = book.book_image.url
        book.downloads += 1
        book.save()
        file            = open(settings.MEDIA_ROOT+"/"+f_file.split('/')[-1], 'rb')
        #wrapper        = FileWrapper(file(file))
        response        = HttpResponse(file.read(), content_type="application/pdf") #mimetypes.guess_type(file)[0])
        #response['Content-Length'] = os.path.getsize(file)
        response['Content-Disposition'] ='attachment; filename=%s'%f_file.split('/')[-1]
        user.downloads  +=1
        user.save()
        return response

def test(request):
    if request.method == 'GET':
        return render(request,'data/test.html')


def upload(request):
    """ Used to store any file to server when not logged to the dashboard """
    if request.method == 'GET':
        return render(request,'data/file.html',{})
    im      = request.FILES['doc']
   
    if im:
        #if request.user.is_superuser:
            path    = os.path.join(settings.MEDIA_ROOT,im.name)
            #image  = req.urlretrieve(url,path)
            savedto = default_storage.save(path,im)
            return HttpResponse("Done")
    return HttpResponse("Error")

def work_thing(request):
    try:
        return render(request, "data/work/soda.html");
    except Exception as error:
        HttpResponse("Oops Oops! That was an error!<hr>%s"%error)


