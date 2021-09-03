from vanidiam.settings import TEMPLATES
from django.shortcuts import render
from django.http import HttpResponse
from django.http import request
from django.conf import settings
from django.core.mail import send_mail
from random import randrange

from .models import User,Event


# Create your views here.

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def advisor(request):
    return render(request, "advisor.html")

def blog(request):
    return render(request, "blog.html")

def contact(request):
    return render(request, "contact.html")

def register(request):
    if request.method == "POST":
        name = request.POST["full-name"]
        email = request.POST['email']
        mob= request.POST['mobile']
        password=request.POST['password']
        cpassword=request.POST['confpassword']

        if password == cpassword:
            global temp
            temp={
                'name': name,
                'email':email,
                'mobile': mob,
                'password': password,
             }
            otp= randrange(1000,9999)
            subject='OTP Verification for VANI DIAM'
            message = f'Hi your otp is {otp}, Thanks for registration'
            email_from= settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list ) 

            return render(request,'otp.html',{'otp':otp})  

        else:
            msg = 'Password and cpassword not matched'
            return render(request,'register.html',{'msg':msg})
        
    else:
        return render(request, "register.html")

def index(request):
    return render(request, "index.html")


def single(request):
    return render(request, "single.html")

def collection(request):
    return render(request, "collection.html")

def dashboard(request):
    return render(request, "dashboard.html")

def fpassword1(request):
    if request.method == "POST":
        email=request.POST['email']
        
        try:
            uid=User.objects.get(email=email)

        except:
            msg= "Email is not registered with us, Enter valid email"
            return render(request,'fpassword1.html', {'msg':msg})
            
        otp= randrange(1000,9999)
        subject='OTP Verification for VANI DIAM'
        message = f'Hi your otp is {otp}, Thanks for registration'
        email_from= settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list ) 

        return render(request,'fpassword2.html',{'otp':otp, 'email':email})  


    return render(request, "fpassword1.html")


def fpassword2(request):
    if request.method == "POST":
        otp=request.POST['otp']
        uotp=request.POST['uotp']
        email=request.POST['email']
        if otp == uotp:
            return render(request, 'fpassword3.html',{'email':email})
        else:
            msg="OTP Does not matched"
            return render(request,'fpassword2.html',{'msg':msg,'otp':otp, 'email': email})

    else: return render(request, 'fpassword2.html',{'otp':otp, 'email':email})

def fpassword3(request):
    if request.method == "POST":
        email= request.POST['email']
        newpassword=request.POST['newpassword']
        confirmpassword=request.POST['confirmpassword']

        if newpassword == confirmpassword:
            uid = User.objects.get(email=email)
            uid.password=newpassword
            uid.save()
            msg="Password changed successfully, please login with new password"
            return render(request, 'login.html',{'msg':msg})
        else:
            msg="Both password should be same" 
            return render(request,'fpassword3.html', {'msg':msg, 'email':email})   

    else:
        return render(request,'fpassword3.html') 

def login(request):
    if request.method == "POST":
        email= request.POST['email']
        password= request.POST['password']
        try: 
            uid= User.objects.get(email= request.POST['email'])
        except:
            msg = 'Enter valid Email'
            return render(request,'login.html',{'msg':msg})

        if password == uid.password:
            request.session['email'] = request.POST['email'] 

            return render(request,'dashboard.html',{'uid': uid})
        else:
            msg = 'Password does not matched'
            return render(request,'login.html',{'msg':msg})

    else:
        return render(request, "login.html")

def logout(request):
    print(request.session['email'])
    del request.session['email']
    
    return render(request,'login.html')



def otp(request):
    if request.method == "POST":
        otp = request.POST['otp']
        uotp = request.POST['uotp']

        if otp == uotp: 
            User.objects.create(
                name=temp['name'],
                email=temp['email'],
                mobile=temp['mobile'],
                password=temp['password']


            )
            return render(request, 'contact.html')
        else: 
            msg= 'Enter correct OTP'
            return render(request, 'otp.html',{'otp':otp, 'msg':msg})    

    else:
        return render(request, "otp.html")




def profile(request):
    email=request.session['email']
    uid = User.objects.get(email=email)

    if request.method=="POST":
        uid.name = request.POST['name']
        uid.mobile = request.POST['mobile']
        uid.email= request.POST['email']
        uid.pic=request.FILES['pic']
        uid.save()
    return render(request, "profile.html",{'uid':uid})



def add_event(request):
    uid = User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        if 'epic' in request.FILES:
            Event.objects.create(
                uid= uid,
                etitle= request.POST['etitle'],
                edate = request.POST['edate'],
                edis= request.POST['edis'],
                epic= request.FILES['epic']
            )
        else: 
            Event.objects.create(
                uid= uid,
                etitle= request.POST['etitle'],
                edate = request.POST['edate'],
                edis= request.POST['edis'],
                )
        msg="EVENT CREATED" 
        return render(request, 'add-event.html',{'uid':uid, 'msg':msg})
    else:
        return render(request, 'add-event.html',{'uid':uid })

def all_event(request):
    uid=User.objects.get(email= request.session['email'])
    events=Event.objects.all()
    return render(request, 'all-event.html', {'events':events, 'uid':uid})


def edit_event(request,pk):
    eid= Event.objects.get(id=pk)
    edate = str(eid.edate)
    if request.method == "POST":
        eid.etitle= request.POST['etitle']
        eid.edate= request.POST['edate']
        eid.edis= request.POST['edis']
        if 'epic' in request.FILES:
            eid.epic = request.FILES['epic']
        eid.save()
        uid = User.objects.get(email= request.session['email'])
        events= Event.objects.all()
        return render(request,'all-event.html', {'events': events, 'uid':uid })
    else:
        return render(request,'edit-event.html', {'eid':eid, 'edate':edate})

def delete_event(request,pk):
    eid=Event.objects.get(id=pk)
    eid.delete()
    uid= User.objects.get(email=request.session['email'])
    events= Event.objects.all()
    return render(request,'all-events.html',{'events':events,'uid':uid})

    