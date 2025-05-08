from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'confirmation', 'email', 'role', 'telephone', 
            'adresse', 'acceptation_CGU', 'user_valide', 'administrateur'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d’utilisateur'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
            'confirmation': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez le mot de passe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'role': forms.Select(attrs={'class': 'form-control', 'id': 'id_role'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            'acceptation_CGU': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'user_valide': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'administrateur': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # Champs supplémentaires (visibles dynamiquement)
    domaine_expertise = forms.CharField(
        max_length=200, required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Domaine d'expertise", 'id': 'id_domaine_expertise'})
    )
    nom_entreprise = forms.CharField(
        max_length=200, required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom de l'entreprise", 'id': 'id_nom_entreprise'})
    )
    nom_agence = forms.CharField(
        max_length=200, required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom de l'agence", 'id': 'id_nom_agence'})
    )

    # Validation personnalisée pour vérifier si la case CGU est cochée
    def clean_acceptation_CGU(self):
        acceptation_CGU = self.cleaned_data.get('acceptation_CGU')
        if not acceptation_CGU:
            raise forms.ValidationError("Vous devez accepter les conditions générales d'utilisation pour vous inscrire.")
        return acceptation_CGU
