from django.db import models

from x.models import Dre

# Create your models here.


class excelsheetsPremiere(models.Model):   
    uid = models.PositiveBigIntegerField()
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    date_naissance = models.CharField(max_length=11,blank=True,null=True)
    prev_ecole = models.CharField(max_length=200,blank=True,null=True)
    prev_ecole_id= models.IntegerField()
    Del1 = models.CharField(max_length=200)
    next_ecole = models.CharField(max_length=200)
    next_ecole_id = models.IntegerField()
    reason= models.CharField(max_length=200)
    decision =models.CharField(max_length=200)
    comments = models.CharField(max_length=200,blank=True,null=True)

    dre = models.ForeignKey(
        Dre, on_delete=models.SET_NULL, blank=True, null=True)
    
    date_downloaded = models.DateField(blank=True,null=True)