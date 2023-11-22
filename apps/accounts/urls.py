from rest_framework.urls import path 
from .  import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('reg_cust/', views.CustomerRegisterView.as_view()),
    path('reg_auth/', views.AuthorRetisterView.as_view()),
    path('act_cust/', views.CustActivationView.as_view()),
    path('act_auth/', views.AuthActivationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),

]