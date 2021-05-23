from django.db import models

# Create your models here.

class Pais(models.Model):
    name=models.CharField(max_length=30)
    ISOS=models.CharField(max_length=30)
    TLD=models.CharField(max_length=30)
    phone_prefix=models.CharField(max_length=30)
    Capital=models.CharField(max_length=30)
    AltNames=models.CharField(max_length=30)
    Region=models.CharField(max_length=30)
    Poblation=models.CharField(max_length=30)
    Coordinates=models.CharField(max_length=30)
    Gentilicio=models.CharField(max_length=30)
    Superficie=models.CharField(max_length=30)
    Gini=models.CharField(max_length=30)
    timezone=models.CharField(max_length=30)
    borderlines=models.CharField(max_length=30)
    native_language=models.CharField(max_length=30)
    codeX=models.CharField(max_length=30)
    coin=models.CharField(max_length=30)
    oficial_language=models.CharField(max_length=30)
    asociations=models.CharField(max_length=30)
    CIOC=models.CharField(max_length=30)
    flag_image=models.ImageField()

    def __unicode__(self):
        return self.name