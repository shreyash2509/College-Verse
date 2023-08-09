

from django.contrib import admin
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import *
from import_export.admin import ImportExportModelAdmin


#-----------------------------------------MYUSER-ADMIN----------------------------------------------------------------------------------------
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'name','profile_img','mobile_number')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password','profile_img','mobile_number', 'name', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name','profile_img','mobile_number', 'is_admin','is_active')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','profile_img','mobile_number',)}),
        ('Permissions', {'fields': ('is_admin','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name','profile_img','mobile_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)





#Register Models



@admin.register(College)
class CollegeAdmin(ImportExportModelAdmin):
    list_display=['id','college_name','branches','exams','location','ownerShip']
    list_editable=['location']
    def branches(self,obj):
        return [ branch for branch in obj.branch_set.all() ]
    def exams(self,obj):
        return [ exam for exam in obj.examsAcceptance.all() ]

    
        

@admin.register(Branch)
class BranchAdmin(ImportExportModelAdmin):
    list_display=['id','college','branch_name']

@admin.register(Exam)
class ExamAdmin(ImportExportModelAdmin):
    list_display=['id','exam_name','categorys','counselling_by']
    def categorys(self,obj):
        return [category for category in obj.category.all()]



@admin.register(CutOFF)
class CutOFFAdmin(ImportExportModelAdmin):
    list_display=['id','exam','branch','hs_or_al','cutoff_by_category','prediction']

@admin.register(Company_wise_placement_detail)
class Company_wise_placement_detailAdmin(ImportExportModelAdmin):
    list_display=['id','college','company','noOfStudentsTaken']
    
@admin.register(Branch_wise_placement_detail)
class Branch_wise_placement_detailAdmin(ImportExportModelAdmin):
    list_display=['id','branch','numberOfStudentsPlaced']

@admin.register(Paper)
class PaperAdmin(ImportExportModelAdmin):
    list_display=['id','exam','paper_name']

@admin.register(Section)
class SectionAdmin(ImportExportModelAdmin):
    list_display=['id','paper','section_name','subject_name','number_of_question','number_of_Questions_to_be_attempted']

@admin.register(MCQTypeQuestion)
class MCQTypeQuestionAdmin(ImportExportModelAdmin):
    list_display=['id','section','question','answer','negetive_marks','option_one','option_two','option_three','option_four','type']
    list_editable=['negetive_marks']



@admin.register(State)
class StateAdmin(ImportExportModelAdmin):
    list_display=['id','state_name']
    list_editable=['state_name']

@admin.register(Counselling)
class CounsellingAdmin(ImportExportModelAdmin):
    list_display=['exam','user','rank','category','get_branches']
    def get_branches(self,obj):
        return [branch for branch in obj.branch.all()]

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display=["id"]

admin.site.register(TestResult)
admin.site.register(Coupon)













