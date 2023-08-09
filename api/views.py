from cgitb import lookup
from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import Branch_wise_placement_detail_Serializer, BranchSerializer,CollegeSerializer,Company_wise_placement_detail_Serializer, CutOFFSerializer,MCQTypeQuestionSerializer
from .serializers import CollegeSerializer
from .models import College,Branch,Company_wise_placement_detail,Branch_wise_placement_detail, MyUser, Section,MCQTypeQuestion,Paper
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser
from rest_framework.pagination import PageNumberPagination
from . import serializers
from .models import Exam,CutOFF
#import permisionclasses
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import generics

#Write your views here.

class CollegeView(APIView):
    parser_classes = [MultiPartParser,FormParser,JSONParser]

    def get(self,request,pk=None):
        if pk is not None:
            college=College.objects.get(id=pk)
            serializer=CollegeSerializer(college)
            return Response(serializer.data)

        colleges=College.objects.all()
        serializer=CollegeSerializer(colleges,many=True)
        return Response(serializer.data)


    def post(self,request):
            
        serializer=CollegeSerializer(data=request.data)
        if serializer.is_valid():
            college=serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        
    def put(self,request):
        college=College.objects.get(id=request.data.get('college_id'))
        for exam_name in request.data.get('examsAcceptance'):
            exam,created=Exam.objects.get_or_create(exam_name=exam_name)
            college.examsAcceptance.add(exam)
        serializer=CollegeSerializer(college)
        return Response(serializer.data)
        
class BranchView(APIView):
    def post(self,request):
        college=College.objects.get(id=request.data.get('college'))
        for branch_name in request.data.get('branch'):
            Branch.objects.create(college=college,branch_name=branch_name)
        serializer=CollegeSerializer(college)
        return Response(serializer.data)
        
class CutOFFView(APIView):
    def post(self,request):
        serializer=CutOFFSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



class CompanyWisePlacementView(APIView):


    def get(self,request):
        college_id=request.data.get("college_id")
        college=College.objects.get(id=college_id)
        if 'ave_salary' in request.query_params:
            companies=Company_wise_placement_detail.objects.filter(college=college).order_by('-averageSalaryOffered')
           
        elif 'median_salary' in request.query_params:
            companies=Company_wise_placement_detail.objects.filter(college=college).order_by('-medianSalaryOffered')
        elif 'no_of_students_taken' in request.query_params:
            companies=Company_wise_placement_detail.objects.filter(college=college).order_by('-noOfStudentsTaken')

        else:
            companies=Company_wise_placement_detail.objects.filter(college=college)
        serializer=Company_wise_placement_detail_Serializer(companies,many=True)
        return Response(serializer.data)




    def post(self,request):
        college=College.objects.get(id=request.data.get('college'))
        serializer=Company_wise_placement_detail_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            Company_wise_placement_detail.objects.create(
                college=college,
                company=request.data.get('company'),
                noOfStudentsTaken=request.data.get('noOfStudentsTaken'),
                minimumSalaryOffered=request.data.get('minimumSalaryOffered'),
                maximumSalaryOffered=request.data.get('maximumSalaryOffered'),
                medianSalaryOffered=request.data.get('medianSalaryOffered')
                )
            return Response(serializer.data)
        return Response(serializer.errors)




class BranchWisePlacementView(APIView):
    def get(self,request):
        branch_id=request.data.get("branch_id")
    
        branch=Branch.objects.get(id=branch_id)
        branch_wise_placement=Branch_wise_placement_detail.objects.get(branch=branch)

        serializer=Branch_wise_placement_detail_Serializer(branch_wise_placement)        
        return Response(serializer.data)
    def post(self,request):
        serializer=Branch_wise_placement_detail_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class RankPredictorView(APIView):
    def get(self,request):
        exam_name = request.data.get('exam')
        hs_or_al=request.data.get('hs_or_al',"")
        category=request.data.get('category',"")
        rank=request.data.get('rank')
        gender=request.data.get('gender',"")
        exam=Exam.objects.get(exam_name=exam_name)
        queryset=CutOFF.objects.filter(
            Q(exam=exam) &
            Q(hs_or_al=hs_or_al)&
            Q(gender=gender) &
            Q(prediction=True)
              )
        queryset=list(queryset.values())
        result=[]
        for element in queryset:
            cutoff_by_category=element['cutoff_by_category']
            temp=cutoff_by_category[category].split("-")
            temp=list(map(int,temp))
            print(temp)
            if rank >= temp[0] and rank <= temp[1]:
                result.append(element)
        return Response(result)



class TestView(APIView):
    def get(self,request):
        section=Section.objects.get(id=request.data.get("section_id"))
        questions=list(section.mcqtypequestions.all().values())
        return Response(questions)

class MCQQuestionView(APIView):
    def get(self,request,pk=None):
        # pagination=PageNumberPagination()
        # pagination.page_size=1
        section=Section.objects.get(id=pk)
        mcqtypequestions=section.mcqtypequestions.all()
        # pagination.paginate_queryset(queryset=mcqtypequestions, request=request)
        # serializer=MCQTypeQuestionSerializer(pagination.paginate_queryset(queryset=mcqtypequestions, request=request),many=True)
        # return pagination.get_paginated_response(serializer.data)
        serializer=MCQTypeQuestionSerializer(mcqtypequestions,many=True)
        return Response(serializer.data)
        
class QuestionView(APIView):
    def get(self,request,pk):
        paper=Paper.objects.get(id=pk)
        sections=paper.section_set.all()

        q1=MCQTypeQuestion.objects.filter(section=sections[0])
        q2=MCQTypeQuestion.objects.filter(section=sections[1])
        q3=MCQTypeQuestion.objects.filter(section=sections[2])
        q=q1.union(q2,q3)
        serializer=MCQTypeQuestionSerializer(q,many=True)
        return Response(serializer.data)



class DeleteUserView(APIView):
    def post(self,request,pk):
        user=MyUser.objects.get(id=pk)
        user.delete()
        return Response({'result':"user has been deleted"})
        



class EditExamView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset = Exam.objects.all()
    serializer_class = serializers.ExamSerializer
    lookup_field = 'id'

class EditPaperView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset = Paper.objects.all()
    serializer_class = serializers.PaperSerializer
    lookup_field = 'id'

class EditSectionView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset = Section.objects.all()
    serializer_class = serializers.SectionSerializer
    lookup_field = 'id'

class EditQuestionView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset = MCQTypeQuestion.objects.all()
    serializer_class = serializers.MCQTypeQuestionSerializer
    lookup_field = 'id'