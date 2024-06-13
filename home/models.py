from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Contact(models.Model):
    email = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return str(self.id)+"_"+self.email
    

class Diagnose(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    text = models.TextField()
    cdr = models.FloatField()
    datetime = models.DateTimeField()

    def __str__(self):
        return str(self.id)+"_"+str(self.username)
    