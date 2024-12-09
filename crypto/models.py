from django.db import models

# Create your models here.
class records(models.Model):
    id=models.IntegerField(primary_key=True)
    g=models.IntegerField()
    b=models.IntegerField()
    l=models.IntegerField()
    r=models.IntegerField()
    bl=models.IntegerField()
    br=models.IntegerField()
    blr=models.IntegerField()
    blri=models.IntegerField()
    msg=models.IntegerField()

class rsa_records(models.Model):
    id=models.IntegerField(primary_key=True)
    n=models.IntegerField()
    p=models.IntegerField()
    q=models.IntegerField()
    phi=models.IntegerField()
    e=models.IntegerField()
    d=models.IntegerField()
    msg=models.IntegerField()