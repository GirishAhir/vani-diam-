from myapp.models import User
from myapp.views import otp
from django.core.checks import messages
from django.utils.translation import templatize
from clientapp.models import client
from django.shortcuts import render
from django.core.mail import send_mail
from random import randrange
from django.conf import settings
from vanidiam.settings import EMAIL_HOST_USER, TEMPLATES
from django.http import HttpResponse
from django.http import request
import myapp

# Create your views here.


def clhome(request):
    return render(request, 'clhome.html')


def clcontact(request):
    return render(request, 'clcontact.html')

def cllogin(request):
    if request.method == "POST":
        email= request.POST['email']
        password= request. POST['password']

        try: 
            uid= client.objects.get(clemail= request.POST['email'])

        except: 
            msg="Email is not registered with us..please register first"
            return render(request,'cllogin.html', {'msg':msg})

        if password == uid.clpassword: 
            request.session['clemail'] = request.POST['email']

            return render(request,'cldash.html',{'uid': uid})

        else:
            msg='Wrong password entered'
            return render(request,'cllogin.html', {'msg':msg})

    else:
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


def cllogout(request):
    print(request.session['clemail'])
    del request.session['clemail']

    return render(request ,'cllogin.html')


def clcollection(request): 
    return render(request, 'clcollection.html')

def clforgot1(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            uid= client.objecets.get(clemail= email)
        except: 
            msg={'Email Not Found'}
            return render (request, 'clforgot1.html', {'msg': msg})
        
        otp = randrange(1000,9999)
        subject = "Confirm OTP for reset password"
        messages= f'Hi , your otp to rest password is {otp}'
        email_from= settings.EMAIL_HOST_USER
        recipient_list=[email,]
        send_mail(subject, messages, email_from, recipient_list )

        return render (request, 'clforgot2.html', {'otp': otp,'email': email })

    else:
        return render(request, 'clforgot1.html')  


def clforgot2(request):
    if request.method == "POST": 
        otp= request.POST['otp']
        clotp= request.POST['clotp']
        email= request.POST['email']
        
        
        if otp == clotp:
            return render(request,'clforgot3.html', {'email': email}) 
        
        else: 
            msg='OPT Not Matched'
            return render(request, 'clforgot2.html', {'otp':otp, 'email': email, 'msg':msg})

    else:
        return render(request, 'clforgot2.html', {'otp': otp, 'email': email})


def clforgot3(request):
    if request.method == "POST":
        email= request.POST['email']
        newpassword= request.POST['newpassword']
        confirmpassword= request.POST['confirmpassword']
        
        if newpassword == confirmpassword: 
            uid= User.objects.get(clemail=email)
            uid.clpassword=newpassword
            uid.save()
            msg="Password changed succesfully, You can logion Now with new password "
            return render(request, 'cllogin.html',{'msg':msg})

        else: 
            msg="Both password should be same"
            return render(request, 'clforgot3.html', {'msg':msg, 'email': email})


    else:
        return render(request, 'clforgot3.html') 




                   










