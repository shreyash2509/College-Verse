from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render,redirect
from django.views import View
import razorpay
from api.models import Branch, College, CounsellingCompany, CutOFF, Exam, MCQTypeQuestion, Order, Paper,Plan, Counselling, Query, Section,State, Subject,TestResult,ClassNotes,PreviousYearQuestionPaper
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import  filterColleges, paginationColleges, searchColleges
from api.models import Coupon
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
logger = logging.getLogger("django")
#razorpay client
client=razorpay.Client(auth=("rzp_live_0VG3dOVwo4de0J","BNaCRk4RvzYohxQ8rbxWyNeQ"))

def home(request):
    states=State.objects.all()
    class_names=ClassNotes.objects.all()
    return render(request,'frontend/index.html',{"states":states,'class_names':class_names})



class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        try:
            brnchs=request.GET.get("branch")
            
            if brnchs == None:
                
                brnchs = None
                branches=Branch.objects.none()
            else:
                brnchs=request.GET.get("branch")
                branches=Branch.objects.filter(branch_name = brnchs)

            dupl_branches = Branch.objects.all().values_list('branch_name', flat=True)
            all_branches = []
            for this in dupl_branches:
                if this not in all_branches:
                    all_branches.append(this)
            

              
            user=request.user
            orders=user.order_set.filter(paid=True)
            Counsellings=Counselling.objects.filter(user=user)
            
            
            testresults=user.testresults.all()
            class_names=ClassNotes.objects.all()
            context={'orders':orders,'all_branches':all_branches,'Counsellings':Counsellings,'branches':branches,'brnchs':brnchs,'testresults':testresults,'class_names':class_names}
            return render(request,'frontend/profile.html',context)
        except Exception as e:
            logger.error("Exception In:  ProfileView")
            messages.success(request,'Something Went Wrong')
            return redirect("home")
    def post(self,request):
        try:
            user = request.user
            profile_img = request.FILES.get('profile_img')
            name = request.POST.get('name')
            ph_number = request.POST.get('ph-number')
            if profile_img:
                user.profile_img = profile_img
            if ph_number :
                user.mobile_number = ph_number
            if name:
                user.name = name
            user.save()
            return redirect('profile')
        except Exception as e:
            logger.error("Exception In:  ProfileView post method")
            messages.success(request,'Something Went Wrong')
            return redirect("home")



class CollegeView(View):
    class_names=ClassNotes.objects.all()
    def get(self,request,pk=None):
        try:
            if pk:
                college=College.objects.get(id=pk)
                branches=college.branch_set.all()
                return render(request,'frontend/overview.html',{"college":college,"class_names":self.class_names,"branches":branches})
            colleges,search_query=searchColleges(request)
            exams=Exam.objects.all()
            college_types=['Government','Private']
            states=State.objects.all()
            
            colleges,exam_id,college_type,location=filterColleges(request,colleges)
            if exam_id:
                exam_id=int(exam_id)
            if location:
                location=int(location)
            colleges,page,custom_range=paginationColleges(request,colleges)
            context={"colleges":colleges,'search_query':search_query,"exams":exams,'college_types':college_types,'states':states,'page':page,'custom_range':custom_range,'exam_id':exam_id,'college_type':college_type,'location':location,"class_names":self.class_names}
            return render(request,'frontend/college.html',context)
        except Exception as e:
            logger.error("Exception In:  CollegeView")
            messages.success(request,'Something went wrong')
            return redirect("home")

discount_price=0#discount_price for coupon code
#coupon code apply view
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

class EcounsellingView(LoginRequiredMixin,View):
    class_names=ClassNotes.objects.all()
    def get(self,request):
        try:
            context={}
            orders=request.user.order_set.filter(paid=True)
            bought_plans=[]
            for order in orders:
                bought_plans.append(order.plan)
            plans=Plan.objects.all()
            context['plans']=plans
            context['bought_plans']=bought_plans
            context['class_names']=self.class_names
            return render(request,'frontend/engineering_1.html',context)
        except Exception as e:
            logger.error("Exception In:  EcounsellingView")
            messages.success(request,'Something went wrong')
            return redirect("home")

    def post(self,request,*args,**kwargs):
        try:
            plan_id=request.POST.get("plan_id")
            plan=Plan.objects.get(id=plan_id)
            coupon_code=request.GET.get("coupon_code",None)
        # print(coupon_code)
            coupon=Coupon.objects.filter(code=coupon_code).first()
            discount_price=0
            if coupon_code is not None:
                discount_price=coupon.discount
                messages.success(request,'Coupon code applied Successfully')
            # else:
            #     messages.success(request,'invalid coupon code')
            #     return redirect("ecounselling")
                # print(discount_price)
            amount=plan.price
            payment=client.order.create({'amount':(amount-discount_price)*100,'currency':"INR",'payment_capture':'1'})
            # Plan.objects.create(user=request.user,plan=plan.upper(),amount=amount//100,order_id=payment['id'])
            Order.objects.create(user=request.user,plan=plan,amount=plan.price,order_id=payment['id'])
            
            context={"payment":payment,"amount":amount-discount_price,"plan":plan,'class_names':self.class_names}
            return render(request,'frontend/payment.html',context)
        except Exception as e:
            logger.error("Exception In:  EcounsellingView post request")
            messages.success(request,'Invalid Coupon Code')
            return redirect("ecounselling")



class McounsellingView(LoginRequiredMixin,View):
    def get(self,request):
        try:
            class_names=ClassNotes.objects.all()
            context={"class_names":class_names}
            return render(request,'frontend/medical_1.html',context)
        except Exception as e:
            logger.error("Exception In:  McounsellingView")
            messages.success(request,'Something went wrong')
            return redirect("home")


class NotesView(LoginRequiredMixin,View):
    class_names=ClassNotes.objects.all()
    def get(self,request,pk=None):
        try:
            class_obj=ClassNotes.objects.get(id=pk)
            subjects=class_obj.subject_set.all()
            return render(request,'frontend/notes11.html',{'subjects':subjects,"class_names":self.class_names})
        except Exception as e:
            logger.error("Exception In:  NotesView")
            messages.success(request,'Something went wrong')
            return redirect("home")

class ChapterView(LoginRequiredMixin,View):
    class_names=ClassNotes.objects.all()
    def get(self,request,pk=None):
        try:
            subject=Subject.objects.get(id=pk)
            chapters=subject.chapter_set.all()
            return render(request,'frontend/phy_notes.html',{'chapters':chapters,"class_names":self.class_names,"subject":subject})
        except Exception as e:
            logger.error("Exception In:  ChapterView")
            messages.success(request,'Something went wrong')
            return redirect("home")

class PreviousYearQuestionPaperView(LoginRequiredMixin,View):
    class_names=ClassNotes.objects.all()
    def get(self,request,pk=None):
        try:
            if pk:
                exam=Exam.objects.get(id=pk)
                previousyearquestionpapers=PreviousYearQuestionPaper.objects.filter(exam=exam).order_by('year')
                return render(request,'frontend/previous-year-questions.html',{"class_names":self.class_names,'previousyearquestionpapers':previousyearquestionpapers})
            exams=Exam.objects.all()
            return render(request,'frontend/notes12.html',{"class_names":self.class_names,'exams':exams})
        except Exception as e:
            logger.error("Exception In:  PreviousYearQuestionPaperView")
            messages.success(request,'Something went wrong')
            return redirect("home")



class PaperView(LoginRequiredMixin,View):
    class_names=ClassNotes.objects.all()
    def get(self,request):
        try:
            context={'class_names':self.class_names}
            if request.GET.get("exam_name"):
                exam=Exam.objects.get(exam_name=request.GET.get("exam_name"))
                papers=exam.paper_set.all()
                user_test_results=TestResult.objects.filter(user=request.user)
                attempted_papers=[]
                for result in user_test_results:
                    attempted_papers.append(result.paper.id)
                papers=papers.exclude(id__in=attempted_papers)
                context['papers']=papers
                #to list all the papers for a exam
                return render(request,'frontend/mtest_1.html',context)
            exams=Exam.objects.all()
            context['exams']=exams
            #to list all the exams
            return render(request,'frontend/test_sel.html',context)
        except Exception as e:
            logger.error("Exception In:  PaperView")
            messages.success(request,'Something went ')
            return redirect("home")

class TestView(LoginRequiredMixin,View):
    class_names=ClassNotes.objects.all()
    def get(self,request,pk):
        try:
            paper=Paper.objects.get(id=pk)
            sections=paper.section_set.all()
            q1=MCQTypeQuestion.objects.filter(section=sections[0])
            q2=MCQTypeQuestion.objects.filter(section=sections[1])
            q3=MCQTypeQuestion.objects.filter(section=sections[2])
            context={}
            context['sections']=sections
            context['q1']=q1
            context['q2']=q2
            context['q3']=q3
            context["paper_id"]=pk
            context['class_names']=self.class_names
            return render(request,'frontend/test_window.html',context)
        except Exception as e:
            logger.error("Exception In:  TestView")
            messages.success(request,'Something went ')
            return redirect("home")

    

def success(request):
    try:
        order_id=request.GET.get("razorpay_order_id","")
        payment_id=request.GET.get("razorpay_payment_id","")
        razorpay_signature=request.GET.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': razorpay_signature
        }
        # verify the payment signature.
        result = client.utility.verify_payment_signature(params_dict)
    
        # plan = Plan.objects.filter(order_id = order_id).first()
        order=Order.objects.filter(order_id=order_id).first()
        order.paid=True
        order.save()
        return redirect("college-prediction")
    except Exception as e:
        logger.error("Exception In:  success view")
        messages.success(request,'Something went wrong')
        return redirect("home")

def failure(request):
    messages.success(request,'Payment Faild')
    return redirect('ecounselling')

class CollegePredictionView(LoginRequiredMixin,View):
    class_names=ClassNotes.objects.all()
    def get(self,request):
        try:
            context={'class_names':self.class_names}
            exam_name=request.GET.get("exam")
            
            
            #form page ro predict college for each exams .
            if exam_name:
                exam_obj=Exam.objects.get(exam_name=exam_name)
                states=State.objects.all()
                categories=exam_obj.category.all()
                context['categories']=categories
                context['states']=states
                if exam_name=="JEE MAIN":
                    context['exam_name']='JEE MAIN'
                elif exam_name=="JEE ADVANCED":
                    context['exam_name']='JEE ADVANCED'
                elif exam_name=="COMEDK":
                    context['exam_name']='COMEDK'
                elif exam_name=="WBJEE":
                    context['exam_name']='WBJEE'
                return render(request,'frontend/college-prediction-form.html',context)
            # Page to select exam for college prediction(dropdown list page)
            queryset=CounsellingCompany.objects.none()
            exams=Exam.objects.none()
            for obj in request.user.order_set.filter(paid=True):
                queryset=queryset.union(obj.plan.counselling_companies.all())
            for obj in queryset:
                exams=exams.union(Exam.objects.filter(counselling_by=obj))
            context['exams']=exams
            context['select_exam']=True
            
            return render(request,'frontend/rank.html',context)


        except Exception as e:
            logger.error("Exception In:  CollegePredictionView")
            messages.success(request,'Something went wrong')
            return redirect("home")
    def post(self,request):
        try:
            exam_name=request.POST.get('exam_name')
            
            category=request.POST.get("category")
            rank=int(request.POST.get("rank"))
            gender=request.POST.get("gender")
            state_id=request.POST.get("state_id")
            
            exam=Exam.objects.get(exam_name=exam_name)
            state=State.objects.get(id=state_id)
            obj,created=Counselling.objects.get_or_create(exam=exam,user=request.user)
            obj.state=state
            obj.category=category
            obj.rank=rank
            obj.gender = gender
            obj.save()
            obj.branch.clear()
            queryset=CutOFF.objects.filter(
                Q(exam=exam) &
                Q(gender=gender) &
                Q(hs_or_al="AI")&
                Q(prediction=True)
                )
            for element in queryset:
                cutoff_by_category=element.cutoff_by_category
                
                temp=cutoff_by_category[category].split("-")
                temp=list(map(int,temp))
                if rank >= temp[0]-1000 and rank <= temp[1]+2000:
                    obj.branch.add(element.branch) 
                    
            return redirect('profile')
        except Exception as e:
            logger.error("Exception In:  CollegePredictionView post request")
            messages.success(request,'Something went wrong')
            return redirect("home")

class ResultView(LoginRequiredMixin,View):
    class_names=ClassNotes.objects.all()
    def get(self,request,pk):
        try:
            result=TestResult.objects.get(id=pk)
            return render(request,'frontend/test-result.html',{'result':result,'total_marks':result.paper.total_marks,'class_names':self.class_names})
        except Exception as e:
            logger.error("Exception In:  ResultView")
            messages.success(request,'Something went wrong')
            return redirect("home")
            
    def post(self,request):
        try:
            paper=Paper.objects.get(id=request.POST.get("paper_id"))
            result_obj=TestResult.objects.filter(user=request.user,paper=paper).first()
            if result_obj:
                messages.success(request,'You already attempted this paper')
                return redirect(reverse('get-results',kwargs={'pk':result_obj.id}))

            result=TestResult.objects.create(
                user=request.user,
                paper=paper,
                correct_questions=request.POST.get("correct_questions"),
                incorrect_questions=request.POST.get("incorrect_questions"),
                total_marks=request.POST.get("score"),
                subject_1=request.POST.get("subject_1"),
                subject_1_marks=request.POST.get("subject_1_marks"),
                subject_2=request.POST.get("subject_2"),
                subject_2_marks=request.POST.get("subject_2_marks"),
                subject_3=request.POST.get("subject_3"),
                subject_3_marks=request.POST.get("subject_3_marks"),
                total_time=request.POST.get("total_time"),
                positive_marks=request.POST.get("positive_marks"),
                negetive_marks=request.POST.get("negetive_marks")
            )
            
            return redirect(reverse('get-results',kwargs={'pk':result.id}))
        except Exception as e:
            logger.error("Exception In:  ResultView post request")
            messages.success(request,'Something went wrong')
            return redirect("home")

class QueryView(View):
    def get(self,request):
        try:
            type=request.GET.get("type")
            name=request.GET.get("name")
            email=request.GET.get("email")
            ph_number=request.GET.get("ph-number")
            wa_number=request.GET.get("wa-number")
            state=State.objects.filter(id=request.GET.get("state")).last()
            message=request.GET.get("message")
            Query.objects.create(
                type=type,
                name=name,
                email=email,
                ph_number=ph_number,
                wa_number=wa_number,
                state=state,
                message=message
            )
            messages.success(request,'Query raised')
            return redirect("home")
        except Exception as e:
            logger.error("Exception In:  QueryView")
            messages.success(request,'Something went wrong')
            return redirect("home")

        
class PrivacyPolicyView(View):
    class_names=ClassNotes.objects.all()
    def get(self,request):
        query=request.GET.get('q')
        if query == 'policy':
            return render(request,'frontend/privacy_pol.html',{'class_names':self.class_names})
        elif query == 'tnc':
            return render(request,'frontend/tnc.html',{'class_names':self.class_names})
        elif query == "refund_policy":
            return render(request,'frontend/refund.html',{'class_names':self.class_names})
        elif query == "contact_us":
            states=State.objects.all()
            return render(request,'frontend/contact.html',{'class_names':self.class_names,"states":states})
        
