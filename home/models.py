from django.db import models
import uuid
# Create your models here.
class Contact(models.Model):
    email = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return str(self.id)+"_"+self.email
    