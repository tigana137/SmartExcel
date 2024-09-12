from django.db import models

from users.models import UserProfile
from x.models import Dre


# Create your models here.


class excelsheets(models.Model):   
    uid = models.PositiveBigIntegerField()
    nom_prenom = models.CharField(max_length=200)
    nom_pere = models.CharField(max_length=200,blank=True,null=True)
    date_naissance = models.CharField(max_length=30,blank=True,null=True)
    level = models.CharField(max_length=11)
    prev_ecole = models.CharField(max_length=200,blank=True,null=True)
    prev_ecole_id= models.IntegerField()
    Del1 = models.CharField(max_length=200)
    next_ecole = models.CharField(max_length=200)
    next_ecole_id = models.IntegerField()
    reason= models.CharField(max_length=200,null=True,blank=True)
    decision =models.CharField(max_length=200,blank=True,null=True)
    decision_id= models.IntegerField()
    comments = models.CharField(max_length=200,blank=True,null=True)
    user = models.ForeignKey(UserProfile,on_delete=models.PROTECT , blank=True, null=True) 
    dre = models.ForeignKey(Dre, on_delete=models.SET_NULL, blank=True, null=True)
    
    date_downloaded = models.DateField(blank=True,null=True)




class excelsheets_brillant(models.Model):   
    uid = models.CharField(max_length=200,null=True,blank=True)
    nom_prenom = models.CharField(max_length=200,null=True,blank=True)
    level = models.CharField(max_length=200,null=True,blank=True)
    prev_ecole = models.CharField(max_length=200,blank=True,null=True)
    Del1 = models.CharField(max_length=200,null=True,blank=True)
    next_ecole = models.CharField(max_length=200,null=True,blank=True)
    reason= models.CharField(max_length=200,null=True,blank=True)
    decision =models.CharField(max_length=200,blank=True,null=True)
    dre = models.ForeignKey(Dre, on_delete=models.SET_NULL, blank=True, null=True)
    
    date_downloaded = models.DateField(blank=True, null=True)
