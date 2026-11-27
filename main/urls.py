from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from main.forms import CustomLoginForm


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html', authentication_form=CustomLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/create/', views.create_application, name='create_app'),
    path('profile/delete/<int:pk>/', views.delete_application, name='delete_app'),
    path('superadmin/', views.admin_panel, name='admin_panel'),
    path('superadmin/user/delete/<int:pk>/', views.delete_user, name='delete_user'),
    path('superadmin/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('superadmin/application/delete/<int:pk>/', views.delete_application_admin, name='delete_app_admin'),
    path('superadmin/status/<int:pk>/<str:new_status>/', views.change_status, name='change_status'),
]