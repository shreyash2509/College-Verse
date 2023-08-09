from operator import truediv
from django.db import models
import statistics
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,AbstractUser,UserManager
)
from django.contrib.auth.hashers import make_password
# Create your models here.

#-------MYUSER-MODEL------
class MyUserManager(BaseUserManager):
    def create_user(self, email,  password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email,  password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff=True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    username=None
    name=models.CharField(max_length=100,null=True,blank=True)
    profile_img = models.ImageField(upload_to='images',null=True,blank=True,default='images/profile-pic.png')
    mobile_number=models.CharField(max_length=50)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email
    def get_full_name(self):
        return self.email   
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class Counselling(models.Model):
    CHOICES2 = (
        ('','---'),
        ("M", "M"),
        ("F", "F"),
        )
    exam=models.ForeignKey('Exam',on_delete=models.CASCADE,blank=True,null=True)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,blank=True,null=True)
    gender=models.CharField(max_length=20,choices=CHOICES2,default="",null=True,blank=True)
    rank=models.IntegerField(null=True,blank=True)
    category=models.CharField(max_length=100,null=True,blank=True)
    state=models.ForeignKey('State',null=True,blank=True,on_delete=models.CASCADE)
    branch=models.ManyToManyField('Branch')
    def __str__(self):
        return self.user.email
    
class State(models.Model):
    state_name=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.state_name

# college Model
class College(models.Model):
    college_name=models.CharField(max_length=100)
    college_image=models.ImageField(upload_to='images',null=True,blank=True,default='images/default.png')
    yearOfEstablishment=models.CharField(max_length=10)
    ownerShip=models.CharField(max_length=100)
    examsAcceptance=models.ManyToManyField('Exam',related_name='examsAcceptance')
    location=models.ForeignKey(State,on_delete=models.CASCADE,null=True,blank=True)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.college_name

class Branch(models.Model):
    branch_name = models.CharField(max_length=255)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    def __str__(self):
        return self.branch_name + ' of ' + self.college.college_name 

class CounsellingCompany(models.Model):
    counselling_company_name=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.counselling_company_name
    
class Exam(models.Model):
    exam_name=models.CharField(max_length=100)
    category=models.ManyToManyField('Category')
    counselling_by=models.ForeignKey(CounsellingCompany,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.exam_name

class CutOFF(models.Model):
    CHOICES = (
        ('','---'),
        ("HS", "HS"),
        ("AI", "AI")
        )
    CHOICES2 = (
        ('','---'),
        ("M", "M"),
        ("F", "F"),
        )
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    prediction=models.BooleanField(default=False)
    gender=models.CharField(max_length=20,choices=CHOICES2,default="",null=True,blank=True)
    hs_or_al=models.CharField(max_length=20,choices=CHOICES,default="")
    cutoff_by_category=models.JSONField()
    def __str__(self):
        return self.exam.exam_name

class Company_wise_placement_detail(models.Model):
    college=models.ForeignKey(College,on_delete=models.CASCADE)
    company=models.CharField(max_length=100)
    noOfStudentsTaken=models.IntegerField()
    minimumSalaryOffered=models.IntegerField(default=0)
    maximumSalaryOffered=models.IntegerField(default=0)
    averageSalaryOffered=models.FloatField(default=0,null=True,blank=True)
    medianSalaryOffered=models.FloatField(default=0,null=True,blank=True)
    def __str__(self):
        return self.company
    def save(self, *args, **kwargs):
        self.averageSalaryOffered= (self.maximumSalaryOffered+self.minimumSalaryOffered)/2
        self.medianSalaryOffered=  statistics.median([self.maximumSalaryOffered,self.minimumSalaryOffered])
        super(Company_wise_placement_detail, self).save(*args, **kwargs)

class Branch_wise_placement_detail(models.Model):
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE)
    numberOfStudentsPlaced=models.IntegerField(default=0,null=True,blank=True)
    yearFrom=models.CharField(max_length=10)
    yearTo=models.CharField(max_length=10)
    def __str__(self):
        return self.branch.branch_name

class Paper(models.Model):
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
    paper_name=models.CharField(max_length=100)
    total_marks=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return str(self.paper_name)+" " + str(self.exam.exam_name)

class Section(models.Model):
    paper=models.ForeignKey(Paper,on_delete=models.CASCADE,null=True,blank=True)
    section_name=models.CharField(max_length=100)
    subject_name=models.CharField(max_length=100)
    number_of_question=models.IntegerField()
    number_of_Questions_to_be_attempted=models.IntegerField(default=0,null=True,blank=True)
    def __str__(self):
        return str(self.paper.exam.exam_name)+" "+ str(self.subject_name) + " " + str(self.id)

class MCQTypeQuestion(models.Model):
    CHOICES = (
        ("MCQ", "MCQ"),
        ("INT", "INT")
        )
    section=models.ForeignKey(Section,on_delete=models.CASCADE,related_name="mcqtypequestions")
    question=models.TextField(blank=True,null=True)
    question_image=models.ImageField(upload_to='images',null=True,blank=True)
    answer=models.CharField(max_length=100, null=True,blank=True)
    candidate_answer=models.IntegerField(null=True,blank=True)          #NO USE
    type=models.CharField(max_length=100,choices=CHOICES,default="MCQ")  
    img_option=models.ImageField(upload_to='images',null=True,blank=True)  #NO USE
    option_one=models.CharField(max_length=100,null=True,blank=True)
    option_two=models.CharField(max_length=100,null=True,blank=True)
    option_three=models.CharField(max_length=100,null=True,blank=True)
    option_four=models.CharField(max_length=100,null=True,blank=True)
    total_marks=models.IntegerField()
    negetive_marks=models.IntegerField()
    @property
    def get_question_image_url(self):
        if self.question_image:
            return self.question_image.url
        return ""
    def __str__(self):
        return self.question


# class IntegerTypeQuestion(models.Model):
#     section=models.ForeignKey(Section,on_delete=models.CASCADE,related_name="integertypequestions")
#     question=models.TextField()
#     question_image=models.ImageField(upload_to='images',null=True,blank=True)
#     answer=models.IntegerField()
#     candidate_answer=models.IntegerField(null=True,blank=True)
#     total_marks=models.IntegerField()
#     negetive_marks=models.IntegerField()
#     def __str__(self):
#         return self.question


class Category(models.Model):
    category_name=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.category_name

class TestResult(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True,related_name="testresults")
    paper=models.ForeignKey(Paper,on_delete=models.CASCADE,null=True,blank=True)
    correct_questions=models.CharField(max_length=100,null=True,blank=True)
    incorrect_questions=models.CharField(max_length=100,null=True,blank=True)
    total_marks=models.CharField(max_length=100,null=True,blank=True)
    subject_1=models.CharField(max_length=100,null=True,blank=True)
    subject_1_marks=models.CharField(max_length=100,null=True,blank=True)
    subject_2=models.CharField(max_length=100,null=True,blank=True)
    subject_2_marks=models.CharField(max_length=100,null=True,blank=True)
    subject_3=models.CharField(max_length=100,null=True,blank=True)
    subject_3_marks=models.CharField(max_length=100,null=True,blank=True)
    total_time=models.CharField(max_length=100,null=True,blank=True)
    positive_marks=models.CharField(max_length=100,null=True,blank=True)
    negetive_marks=models.CharField(max_length=100,null=True,blank=True)

class Plan(models.Model):
    plan_name=models.CharField(max_length=100,null=True,blank=True)
    heading=models.CharField(max_length=100,null=True,blank=True)
    desc1=models.CharField(max_length=100,null=True,blank=True)
    desc2=models.CharField(max_length=100,null=True,blank=True)
    desc3=models.CharField(max_length=100,null=True,blank=True)
    desc4=models.CharField(max_length=100,null=True,blank=True)

    price=models.IntegerField(default=0,null=True,blank=True)
    counselling_companies=models.ManyToManyField(CounsellingCompany)
    def __str__(self):
        return str(self.plan_name)

class Order(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    plan=models.ForeignKey(Plan,on_delete=models.CASCADE,null=True,blank=True)
    amount=models.CharField(max_length=100)
    order_id=models.CharField(max_length=100)
    paid=models.BooleanField(default=False)

class Query(models.Model):
    CHOICES = (
        ("get_in_touch", "get_in_touch"),
        ("medical_call", "medical_call")
        )
    type=models.CharField(max_length=100,choices=CHOICES)
    name=models.CharField(max_length=100,null=True,blank=True)
    email=models.CharField(max_length=100,null=True,blank=True)
    ph_number=models.CharField(max_length=100,null=True,blank=True)
    wa_number=models.CharField(max_length=100,null=True,blank=True)
    state=models.ForeignKey(State,on_delete=models.CASCADE,null=True,blank=True)
    message=models.TextField(null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    class Meta:
        ordering = ['-date_created']
    def __str__(self):
        return str(self.ph_number)

class ClassNotes(models.Model):
    CHOICES = (
        ("XI", "XI"),
        ("XII", "XII")
        )
    class_name=models.CharField(max_length=100,choices=CHOICES,null=True,blank=True)
    def __str__(self):
        return self.class_name

class Subject(models.Model):
    subject_name=models.CharField(max_length=100,null=True,blank=True)
    class_obj=models.ForeignKey(ClassNotes,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return str(self.subject_name) + "of class " + str(self.class_obj.class_name)

class Chapter(models.Model):
    chapter_name=models.CharField(max_length=100,null=True,blank=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return str(self.chapter_name)+ " of " +str(self.subject.subject_name)

class PDF(models.Model):
    CHOICES = (
        ("DPP", "DPP"),
        ("Chapter Wise Notes", "Chapter Wise Notes"),
        ('Mind Map','Mind Map')
        )
    type=models.CharField(max_length=100,null=True,blank=True,choices=CHOICES)
    file=models.FileField(upload_to='images',null=True,blank=True)
    chapter=models.ForeignKey(Chapter,on_delete=models.CASCADE,null=True,blank=True)


class PreviousYearQuestionPaper(models.Model):
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE,null=True,blank=True)
    year=models.DateField(null=True,blank=True)
    file=models.FileField(upload_to='images',null=True,blank=True)

    



#Login signal
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.signals import user_logged_in 

def djangologinSignal(sender,request,user,**kwargs):
    obj=SocialAccount.objects.filter(user=user).last()
    if obj:
        name=obj.extra_data.get('name')
        if name:
            user.name=name
            user.save()
user_logged_in.connect(djangologinSignal,sender=MyUser)


class Coupon(models.Model):
    code=models.CharField(max_length=20,null=True,unique=True)
    discount=models.IntegerField(default=0)
    valid_from=models.DateField(null=True,blank=True)
    valid_to=models.DateField(null=True,blank=True)
    def __str__(self):
        return self.code
    

    












    


    




    










