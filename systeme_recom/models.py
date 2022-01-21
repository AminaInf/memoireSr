from django.contrib.auth.models import User
from django.db import models

from .current_user import get_current_user


class Region(models.Model):
    nomRegion = models.CharField(max_length=50)

    def __str__(self):
        return self.nomRegion

class UserProfile(models.Model):
    user = models.ForeignKey('auth.User', default=get_current_user,on_delete=models.CASCADE)
    ID_NCULTURE = models.CharField(max_length=140)
    ID_VARIETE = models.CharField(max_length=140)
    ID_RENDEMENT = models.CharField(max_length=140)
    ID_HUMIDITE = models.CharField(max_length=140)
    ID_CM = models.CharField(max_length=140)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    #profile_picture = models.ImageField(upload_to='thumbpath', blank=True)
    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

class Culture(models.Model):
    user = models.ForeignKey('auth.User', default=get_current_user,on_delete=models.CASCADE)
    variete = models.CharField(max_length=50)
    nomCulture = models.CharField(max_length=50)
    typeCulture = models.CharField(max_length=50)
    rendement = models.CharField(max_length=50)
    sol = models.CharField(max_length=50)
    ph = models.PositiveIntegerField()
    humidite = models.CharField(max_length=50)
    temperature = models.CharField(max_length=50)
    cycleDeMaturation = models.CharField(max_length=50)

    def __str__(self):
        return self.nomCulture


class Pluviometrie(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    valeur = models.CharField(max_length=50)
    mois = models.CharField(max_length=50)



class Temperature(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    valeur = models.CharField(max_length=50)
    mois = models.CharField(max_length=50)