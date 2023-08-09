import hashlib
from api.models import College,Exam,State
from django.core.paginator import Paginator
import os
def searchColleges(request):
        search_query=''
        if request.GET.get("q"):
            search_query=request.GET.get("q")

        colleges=College.objects.distinct().filter(college_name__icontains=search_query)
        return colleges,search_query
def filterColleges(request,colleges):
    if request.GET.get("exam_id"):
        exam=Exam.objects.get(id=request.GET.get("exam_id"))
        colleges=exam.examsAcceptance.all()
    if request.GET.get("college-type"):
        colleges=colleges.filter(ownerShip=request.GET.get("college-type"))
    if request.GET.get("location"):
        state=State.objects.get(id=request.GET.get("location"))
        colleges=colleges.filter(location=state)    
    return colleges,request.GET.get("exam_id"),request.GET.get("college-type"),request.GET.get("location")

def paginationColleges(request,colleges):
    paginator=Paginator(colleges,6)
    page=request.GET.get('page',1)
    colleges=paginator.get_page(page)
    leftIndex=int(page)-4
    if leftIndex<1:
        leftIndex=1
    
    rightIndex=int(page)+5
    if rightIndex>paginator.num_pages:
        rightIndex=paginator.num_pages
    
    custom_range=range(leftIndex,rightIndex+1)
    return colleges,page,custom_range

def get_google_creds(request,context={}):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    host=request.get_host()
    redirect_uri=f"{protocol}://{host}/accounts/google/login/callback/"
    client_id="80395468994-7gt8mn9785mrhrr1u02c5hou8a7edkk5.apps.googleusercontent.com"
    scope="profile email"
    response_type='code'
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    access_type='online'
    flowName='GeneralOAuthFlow'
    url=f'https://accounts.google.com/o/oauth2/auth/oauthchooseaccount'
    d={'redirect_uri':redirect_uri,"client_id":client_id,"scope":scope,"response_type":response_type,"state":state,'access_type':access_type,"flowName":flowName,"url":url}
    context.update(d)
    return context


# def validate_mobile_number(mobile_number):
#     mobile_number = mobile_number.strip()
#     try:
#         if not mobile_number.startswith("+91"):
#             mobile_number="+91"+mobile_number
#         x = phonenumbers.parse(mobile_number)
#         return phonenumbers.is_valid_number(x)
#     except:
#         return False