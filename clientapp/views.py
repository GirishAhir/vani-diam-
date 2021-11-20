from myapp.models import User, product
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
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum



# Create your views here.


def clhome(request):
    return render(request, 'clhome.html')


def clcontact(request):
    return render(request, 'clcontact.html')

def cllogin(request):
    if request.method == "POST":
        email= request.POST['email']
        password= request.POST['password']

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
     products= product.objects.all()
     return render(request, "clcollection.html" ,{ 'products':products})

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



def clsingle_pd(request, jk):
        prod= product.objects.get(id=jk)
        return render(request, 'clsinglepd.html',{'products':prod})
                   



def cldash(request):
    return render(request, 'cldash.html')


def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'clpay.html') 
        
    amount = int(request.POST['amount'])
    transaction = Transaction.objects.create(amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str('GBAHIR094@GMAIL.COM')),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)




@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'clcallback.html', context=received_data)
        return render(request, 'clcallback.html', context=received_data)







