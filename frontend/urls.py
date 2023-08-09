from django.urls import path,include,re_path
from . import views
from . import auth_views
from django.contrib.auth import views as default_auth_views

from allauth.account.views import *
urlpatterns = [
  path('',views.home,name="home"),
  path('profile',views.ProfileView.as_view(),name="profile"),
  path('colleges/',views.CollegeView.as_view(),name="colleges"),
  path('college/<int:pk>',views.CollegeView.as_view(),name="college"),
  path('ecounselling/',views.EcounsellingView.as_view(),name="ecounselling"),
  path('mcounselling/',views.McounsellingView.as_view(),name="mcounselling"),
  path('notes/<int:pk>/',views.NotesView.as_view(),name="note"),
  path('chapers/<int:pk>/',views.ChapterView.as_view(),name="chapters"),
  path('previous-year-questions/',views.PreviousYearQuestionPaperView.as_view(),name="previous-year-questions"),
  path('previous-year-question/<int:pk>/',views.PreviousYearQuestionPaperView.as_view(),name="previous-year-question"),
  path("test-series/",views.PaperView.as_view(),name="test-series"),
  path("test-series/<int:pk>/",views.TestView.as_view(),name="test"),
  path("success/",views.success,name="success"),
  path("failure/",views.failure,name="failure"),
  path('college-prediction',views.CollegePredictionView.as_view(),name="college-prediction"),
  path('result/',views.ResultView.as_view(),name="result"),
  path('get-results/<int:pk>/',views.ResultView.as_view(),name="get-results"),
  path('query/',views.QueryView.as_view(),name="query"),
  path('legal/',views.PrivacyPolicyView.as_view(),name="legal"),
  #AUth URL
  path('accounts/password/reset/',PasswordResetView.as_view(template_name='password/password_reset.html'),name='account_reset_password'),
  path('accounts/password/reset/done/',PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),name='account_reset_password_done'),
  re_path(r"^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", PasswordResetFromKeyView.as_view(template_name='password/password_reset_confirm.html'), name='account_reset_password_from_key'),
   path('accounts/password/reset/key/done/', PasswordResetFromKeyDoneView.as_view(template_name='password/password_reset_complete.html'), name='account_reset_password_from_key_done'),
  path("signup/",auth_views.SignUpView.as_view(),name="signup"),
  path('login/',auth_views.LoginView.as_view(),name="login"),
  path("logout/",auth_views.logoutView,name="logout"),
  path("verification/<int:pk>/",auth_views.verificationView,name="verification"),
  path('accounts/', include('allauth.urls'),name="social"),


]