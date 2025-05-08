from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator

import user
from .models import Profile  # Assure-toi que `User` est bien ton modèle d'utilisateur personnalisé
from .forms import CustomUserCreationForm
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser  # Importer le modèle CustomUser si nécessaire
User = get_user_model()


# Create your views here.
def accueil(request):
    return render(request,'pigic/page.html')

def dashboard_locataire(request):
    return render(request,'locataire/dashboard_locataire.html')


def dashboard_agent(request):
    return render(request,'agent_immobilier/dashboard_agent.html')


def dashboard_chef(request):
    return render(request,'chef_chantier/dashboard_chef.html')


def dashboard_proprietaire(request):
    return render(request,'proprietaire/dashboard_proprietaire.html')

class SignUpView(CreateView): 
    form_class = CustomUserCreationForm
    template_name = 'pigic/register.html'  
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])  # Hash du mot de passe
        user.user_valide = False  # L'utilisateur doit activer son compte
        user.save()
        
        Profile.objects.create(user=user)  # Création du profil

        # Envoi de l'email d'activation
        self.send_activation_email(user)

        return redirect('activation_sent')  # Page informant que l'email a été envoyé

    def send_activation_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(self.request).domain
        activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        activation_url = f'http://{domain}{activation_link}'

        subject = "Activation de votre compte"
        message = render_to_string('pigic/activation_email.html', {
            'user': user,
            'activation_url': activation_url
        })

        send_mail(subject, message, 'noreply@pigic.com', [user.email])

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.user_valide = True  # Active le compte
            user.save()
            messages.success(request, "Votre compte a été activé avec succès. Vous pouvez maintenant vous connecter.")
            return redirect('login')
        else:
            messages.error(request, "Le lien d'activation est invalide ou a expiré.")
            return redirect('activation_failed')  # Redirection vers une page d'erreur

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authentifier directement avec `authenticate`
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.user_valide:  # Vérifie si l'utilisateur est validé
                login(request, user)  # Connexion

                # Redirection selon le rôle
                redirections = {
                    "locataire": "dashboard_locataire",
                    "proprietaire": "dashboard_proprietaire",
                    "agent_immo": "dashboard_agent",
                    "entrepreneur": "dashboard_chef",
                }
                return redirect(redirections.get(user.role, "page"))  # Redirection dynamique

            else:
                messages.error(request, "Votre compte n'a pas encore été validé.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, "pigic/login.html")  # Formulaire de connexion

def tarification(request):
    return render(request,'pigic/tarification.html')


















# views.py
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.views.generic import FormView

class CustomPasswordResetView(PasswordResetView):
    template_name = 'pigic/password_reset.html'
    email_template_name = 'pigic/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'pigic/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'pigic/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'pigic/password_reset_complete.html'
