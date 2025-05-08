from django.db import models
from django.contrib.auth.models import AbstractUser

# Modèle utilisateur personnalisé
class CustomUser(AbstractUser):
    telephone = models.CharField(max_length=10, blank=True, null=True)
    adresse = models.CharField(max_length=200, blank=True, null=True)
    confirmation = models.CharField(max_length=10, blank=True, null=True)
    
    USER_TYPE_CHOICES = [
        ('proprietaire', 'PROPRIETAIRE'),
        ('locataire', 'LOCATAIRE'),
        ('agent_immo', 'AGENT_IMMO'),
        ('entrepreneur', 'ENTREPRENEUR'),
    ]
    role = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='proprietaire')
    acceptation_CGU = models.BooleanField(default=False)
    user_valide = models.BooleanField(default=False)
    administrateur = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# Modèle de profil utilisateur
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    domaine_expertise = models.CharField(max_length=200, blank=True, null=True)
    nom_entreprise = models.CharField(max_length=200, blank=True, null=True)
    nom_agence = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Profile de {self.user.username}"

# Modèle pour le type de bien
class TypeDeBien(models.Model):
    APPARTEMENT_CHOICES = [
        ('atelier', 'Atelier'),
        ('boutique', 'Boutique'),
        ('maison', 'Maison'),
        ('parking', 'Parking'),
    ]
    designation = models.CharField(max_length=255)
    description = models.TextField()
    appartements = models.CharField(max_length=50, choices=APPARTEMENT_CHOICES)

    def __str__(self):
        return self.designation

# Modèle pour le propriétaire
class Proprietaire(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='proprietaire')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    adresse = models.TextField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"

# Modèle pour le bien immobilier
class Bien(models.Model):
    USAGE_CHOICES = [
        ('residentiel', 'Résidentiel'),
        ('commercial', 'Commercial'),
        ('industriel', 'Industriel'),
        ('mixte', 'Mixte'),
    ]

    STATUT_CHOICES = [
        ('disponible', 'Disponible en location'),
        ('vendu', 'Vendu'),
        ('reserve', 'Réservé'),
        ('en_attente', 'En attente de validation'),
    ]

    reference = models.CharField(max_length=50, unique=True,default=1)
    titre = models.CharField(max_length=200)
    statut = models.CharField(max_length=255, default="disponible")
    surface_totale = models.DecimalField(max_digits=10, decimal_places=2,default=0.0 )
    surface_habitable = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    nombre_pieces = models.IntegerField(null=True, blank=True)
    annee_construction = models.IntegerField(null=True, blank=True)
    etat_bien = models.CharField(max_length=100, null=True, blank=True)
    materiaux_construction = models.CharField(max_length=200, null=True, blank=True)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix_location = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    periodicite_location = models.CharField(max_length=50, null=True, blank=True)
    charges_mensuelles = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    taxe_fonciere = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mode_paiement_accepte = models.CharField(max_length=200, null=True, blank=True)
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE, related_name='biens', null=True, blank=True)
    type_de_bien = models.ForeignKey(TypeDeBien, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titre

# Modèle pour la localisation du bien
class Localisation(models.Model):
    bien = models.OneToOneField(Bien, on_delete=models.CASCADE, related_name='localisation')
    adresse_complete = models.TextField()
    quartier = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    commune = models.CharField(max_length=100)
    prefecture = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.bien.titre} - {self.adresse_complete}"

# Modèle pour le locataire
class Locataire(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='locataire')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    adresse = models.TextField()
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE, related_name='locataires')

    def __str__(self):
        return f"{self.prenom} {self.nom}"

# Modèle pour la facture
class Facture(models.Model):
    locataire = models.ForeignKey(Locataire, on_delete=models.CASCADE, related_name='factures')
    date_emission = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()

    def __str__(self):
        return f"Facture {self.id} - {self.locataire}"

# Modèle pour le contrat
class Contrat(models.Model):
    TYPE_CONTRAT_CHOICES = [
        ('location', 'Location'),
        ('vente', 'Vente'),
        ('bail', 'Bail'),
        ('gestion', 'Gestion'),
    ]

    STATUT_CONTRAT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('desiste', 'Désisté'),
        ('expire', 'Expiré'),
    ]

    SOUS_LOCATION_CHOICES = [
        ('autorise', 'Autorisé'),
        ('interdit', 'Interdit'),
    ]

    numero_contrat = models.CharField(max_length=50)
    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT_CHOICES)
    date_signature = models.DateField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    duree_contrat = models.CharField(max_length=50)
    statut_contrat = models.CharField(max_length=20, choices=STATUT_CONTRAT_CHOICES)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mode_paiement = models.CharField(max_length=100)
    periodicite_paiement = models.CharField(max_length=50)
    caution = models.DecimalField(max_digits=10, decimal_places=2)
    frais_urgence = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    penalites_retard = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    clause_resiliation_anticipee = models.TextField(null=True, blank=True)
    clause_revision_prix = models.TextField(null=True, blank=True)
    clause_entretien = models.TextField(null=True, blank=True)
    clause_sous_location = models.CharField(max_length=20, choices=SOUS_LOCATION_CHOICES, default='interdit')
    assurance = models.TextField(null=True, blank=True)
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE, related_name='contrats')

    def __str__(self):
        return f"Contrat {self.numero_contrat} - {self.type_contrat}"