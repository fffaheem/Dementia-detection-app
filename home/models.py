from django.db import models
import uuid
# Create your models here.
class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.email +"_"+str(self.id)