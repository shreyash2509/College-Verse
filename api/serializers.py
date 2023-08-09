
from rest_framework import serializers
from .models import College,Branch,Company_wise_placement_detail,Branch_wise_placement_detail, CutOFF, Exam, MyUser, Paper, Section,MCQTypeQuestion

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model=Branch
        fields=['id','branch_name']

class CutOFFSerializer(serializers.ModelSerializer):
    class Meta:
        model=CutOFF
        fields="__all__"

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model=Exam
        fields=['id','exam_name']
class CollegeSerializer(serializers.ModelSerializer):

    location=serializers.SlugRelatedField(read_only=True,slug_field='state_name')
    branch=serializers.SerializerMethodField(method_name='get_branches')
    examsAcceptance=ExamSerializer(many=True,required=False)
    class Meta:
        model=College
        fields=['id','college_name','college_image','branch','yearOfEstablishment','ownerShip','examsAcceptance','location']
    def create(self, validated_data):
        
        instance=College.objects.create(
            college_name=validated_data.get("college_name"),
            college_image=validated_data.get("college_image"),
            yearOfEstablishment=validated_data.get("yearOfEstablishment"),
            ownerShip=validated_data.get("ownerShip"),
            location=validated_data.get("location")
            )
        return instance


    def get_branches(self,obj):
        branches=obj.branch_set.all()
        serializer=BranchSerializer(branches,many=True)
        return serializer.data


    


class Company_wise_placement_detail_Serializer(serializers.ModelSerializer):
    college=serializers.StringRelatedField()
    class Meta:
        model=Company_wise_placement_detail
        fields=['college','company','noOfStudentsTaken','minimumSalaryOffered','maximumSalaryOffered','medianSalaryOffered']
        
class Branch_wise_placement_detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Branch_wise_placement_detail
        fields="__all__"


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'name',
                  'email', 'stream','mobile_number', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }
    
class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model=Paper
        fields="__all__"

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Section
        fields="__all__"

class MCQTypeQuestionSerializer(serializers.ModelSerializer):
    section=serializers.SlugRelatedField(read_only=True,slug_field='subject_name')
    class Meta:
        model=MCQTypeQuestion
        fields="__all__"


