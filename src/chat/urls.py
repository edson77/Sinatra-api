from django.urls import path, include
from .views import RegisterView,LoginView,ImageView, usersView, authUserInfoView, ChangePasswordView,Logout,allUsers,userInfoView
from .views import MessageView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    # path('test/',TestView.as_view()),
    path('profile-image/',ImageView.as_view()),
    path('list-users/',usersView.as_view()),
    path('user-infos/',authUserInfoView.as_view()),
    path('user-infos/<int:user_id>/',userInfoView.as_view()),
    path('reset-password/',ChangePasswordView.as_view()),
    path('logout/',Logout.as_view()),
    path('all-users/',allUsers.as_view()),
    path('user-message/<int:id>/',MessageView.as_view()),
   # path('login/', obtain_auth_token, name='obtain-auth-token')
]