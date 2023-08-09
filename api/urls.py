from django.urls import path
from . import views

urlpatterns = [
    path('college/',views.CollegeView.as_view()),
    path('college/<int:pk>/',views.CollegeView.as_view()),
    path('branch/',views.BranchView.as_view()),
    path('company-wise-placement/',views.CompanyWisePlacementView.as_view()),
    path('branch-wise-placement/',views.BranchWisePlacementView.as_view()),
    path('cutoff/',views.CutOFFView.as_view()),
    path('rank-prediction/',views.RankPredictorView.as_view()),
    path('test/',views.TestView.as_view()),
    #to get all mcq questions in a section
    path('section/mcqquestion/<int:pk>/',views.MCQQuestionView.as_view()),
    path('paper/questions/<int:pk>/',views.QuestionView.as_view()),
    path('user/delete/<int:id>/',views.DeleteUserView.as_view()),
    path('edit-exam/<int:id>/',views.EditExamView.as_view()),
    path('edit-section/<int:id>/',views.EditSectionView.as_view()),
    path('edit-question/<int:id>/',views.EditQuestionView.as_view()),
    path('edit-paper/<int:id>/',views.EditPaperView.as_view()),

]
