from django.urls import path
from . import views
from .views import SignUpView, ActivateAccountView
from django.views.generic import TemplateView
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView


urlpatterns = [
    path('',views.accueil, name='accueil'),
    path('locataire', views.dashboard_locataire, name='dashboard_locataire'),
    path('agence', views.dashboard_agent, name='dashboard_agent'),
    path('chef', views.dashboard_chef, name='dasbhoard_chef'),
    path('proprietaire', views.dashboard_proprietaire, name='dashboard_proprietaire'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path("login/",views.login_view, name="login"),
    path("tarification",views.tarification, name="tarification"),
    path('activation-sent/', TemplateView.as_view(template_name='pigic/activation_sent.html'), name='activation_sent'),
    path('activate/<uidb64>/<token>/',ActivateAccountView.as_view(), name='activate'),






    path('mot-de-passe-oublie/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('mot-de-passe-oublie/termine/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reinitialiser/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reinitialiser/termine/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]




