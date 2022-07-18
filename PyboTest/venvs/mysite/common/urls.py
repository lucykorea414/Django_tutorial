from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/base/<int:user_id>/', views.profile_base, name='profile_base'),
    path('profile/question/<int:user_id>/', views.ProfileQuestionListView.as_view(), name='profile_question'),
    path('profile/answer/<int:user_id>/', views.ProfileAnswerListView.as_view(), name='profile_answer'),
    path('profile/comment/<int:user_id>/', views.ProfileCommentListView.as_view(), name='profile_comment'),
    path('profile/vote/<int:user_id>/', views.ProfileVoteListView.as_view(), name='profile_vote'),
]