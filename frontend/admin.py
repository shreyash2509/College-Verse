from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from api.models import CounsellingCompany, Order, Plan,Query,ClassNotes,Subject,Chapter,PDF,PreviousYearQuestionPaper,MyUser
admin.site.unregister(MyUser)

# Register your models here.



@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    list_display=['id','user','plan','amount','order_id','paid']

@admin.register(MyUser)
class MyUserAdmin(ImportExportModelAdmin):
    list_display=['email','name','profile_img','mobile_number','is_active','is_admin']

@admin.register(Plan)
class PlanAdmin(ImportExportModelAdmin):
    list_display=['id','plan_name','price','get_counselling_companies']
    def get_counselling_companies(self,obj):
        return [cmp for cmp in obj.counselling_companies.all()]

@admin.register(CounsellingCompany)
class CounsellingCompanyAdmin(ImportExportModelAdmin):
    list_display=['id','counselling_company_name']

@admin.register(Query)
class QueryAdmin(ImportExportModelAdmin):
    list_display=['id','type','name','email','ph_number','wa_number','date_created']
    list_filter = ("type",)

class PDFAdmin(ImportExportModelAdmin):
    list_display=['id','type','file','chapter']

class PreviousYearQuestionPaperAdmin(ImportExportModelAdmin):
    list_display=['id','exam','year','file']

class ClassNotesAdmin(ImportExportModelAdmin):
    list_display=['id','class_name']

class SubjectAdmin(ImportExportModelAdmin):
    list_display=['id','subject_name','class_obj']

class ChapterAdmin(ImportExportModelAdmin):
    list_display=['id','chapter_name','subject']

admin.site.register(ClassNotes,ClassNotesAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Chapter,ChapterAdmin)
admin.site.register(PDF,PDFAdmin)
admin.site.register(PreviousYearQuestionPaper,PreviousYearQuestionPaperAdmin)