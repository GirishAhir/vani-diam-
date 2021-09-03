from django.utils.translation import templatize
from clientapp.models import client
from django.shortcuts import render
from django.core.mail import send_mail
from random import randrange
from django.conf import settings
from vanidiam.settings import TEMPLATES
from django.http import HttpResponse
from django.http import request

# Create your views here.


def clhome(request):
    return render(request, 'clhome.html')

def cllogin(request):
    return render(request, 'cllogin.html')

def clabout(request):
    return render(request, 'clabout.html')

def clregister(request):
    if request.method == "POST": 
        try: 
            uid = client.objects.get(clemail=request.POST['email'])
            msg = 'Email is already register'

            return render(request,'clregister.html',{'msg':msg})
        except:
            clname=request.POST['clname'],
            email=request.POST['email'],
            mob=request.POST['mobile'],
            add=request.POST['address'],
            compname=request.POST['compname'],
            position=request.POST['position'],
            password=request.POST['password'],
            confpassword=request.POST['confpassword'],

            if password == confpassword:
                global temp
                temp={
                    'clname':clname,
                    'clemail':email,
                    'clmob':mob,
                    'cladd': add,
                    'compname':compname,
                    'position': position,
                    'clpassword':password,
                    }
                print(email)

                otp= randrange(1000,9999)
                subject='OTP Verification for VANI DIAM'
                message = f'Hi your otp is {otp}, Thanks for registration'
                email_from= settings.EMAIL_HOST_USER
                recipient_list = [email, ]
                print('######################################')
                send_mail(subject, message, email_from, recipient_list )

                return render(request,'clotp.html',{'otp':otp})  

            else:
                msg = 'Password and cpassword not matched'
                return render(request,'clregister.html',{'msg':msg})
    else:
        return render(request,'clregister.html')
        
def clotp(request):
    if request.method == "POST":
        print("##############################")
        otp = request.POST['otp']
        uotp = request.POST['uotp']

        if otp == uotp: 
            client.objects.create(
                clname=temp['clname'],
                email=temp['email'],
                mob=temp['mobile'],
                add=temp['address'],
                compname=temp['compname'],
                position=temp['position'],
                password=temp['password'],
                confpassword=temp['confpassword'],
                )
            return render(request, 'clhome.html')
        else: 
            msg= 'Enter correct OTP'
            return render(request, 'clotp.html',{'otp':otp, 'msg':msg})    

    else:
        return render(request, "clotp.html")


