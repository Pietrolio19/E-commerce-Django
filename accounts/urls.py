from django.contrib.auth.views import LoginView
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ProfileView, SignUpView

app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view() , name='profile'),
]