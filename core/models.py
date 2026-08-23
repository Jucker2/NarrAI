from django.db import models

import uuid

# Create your models here.
class Book(models.Model):

    class Status(models.TextChoices):
        UPLOADED="uploaded","Uploaded"
        PROCESSING="processing","Processing"
        COMPLETED="completed","Completed"
        FAILED="failed","Failed"

    uuid=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=255,blank=True)

    language=models.CharField(max_length=20,blank=True)
    pdf= models.FileField(upload_to="Books/")
    status=models.CharField(max_length=20,default=Status.UPLOADED,choices=Status.choices)
    created_at=models.DateTimeField(auto_now_add=True)
    uploaded_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title