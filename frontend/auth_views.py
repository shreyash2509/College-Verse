from django.shortcuts import redirect, render,HttpResponseRedirect
from api.models import MyUser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
import logging
logger = logging.getLogger("django")

class SignUpView(View):
    def post(self,request):
        name=request.POST.get("name")
        mobile_number=request.POST.get("mobile_number")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")
        if password!=confirm_password:
            messages.success(request,'password did not match')
            return redirect("home")
        try:
            user=MyUser.objects.create_user(email,password)
            user.name=name
            user.mobile_number=mobile_number
            user.is_active=False
            user.save()
            try:
                url_link=str(request.build_absolute_uri(reverse("verification", kwargs={'pk':user.id})))
                subject = 'Activate your account'
                message = f'Hi {user.name}, Please click on the link below to activate your account \n {url_link}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                send_mail( subject, message, email_from, recipient_list )
                messages.success(request,'Account has been created, please verify your email.')
                return redirect("home")
            except Exception as e:
                logger.error("Exception In:  Signupview error in sending mail")
                messages.success(request,'Somethig Went Wrong')
                return redirect("home")
        except Exception as e:
            logger.error("Exception In:  Signupview email aleady exist")
            messages.success(request,'User with this email already exist')
            return redirect("home")

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self,request):
        try:
            email=request.POST.get("email")
            password=request.POST.get("password")
            user=authenticate(
                email=email,
                password=password
            )
            if user is not None:
                if user.is_active==True:
                    login(request,user)
                    messages.success(request,'user logged in')
                    if request.POST.get("next"):
                        return HttpResponseRedirect(request.POST.get("next"))
                    else:
                        return redirect("home")
                else:
                    messages.success(request,'Account verification prnding')
                    return redirect("home")
            messages.success(request,'please fill the correct details. make sure you verified your email.')
            return redirect("home")
        except Exception as e:
            logger.error("Exception In:  LoginView")
            messages.success(request,'Please login again')
            return redirect("home")
      

def logoutView(request):
    logout(request)
    messages.success(request,'User logged out')
    return redirect("home")


def verificationView(request,pk):
    try:
        user=MyUser.objects.get(id=pk)
        user.is_active=True
        user.save()
        messages.success(request,'Your account is verified successfully, you can login')
        return redirect('home')
    except Exception as e:
        logger.error("Exception In:  verificationView")
        messages.success(request,'Account verification failed')
        return redirect("home")
        

             

        
        