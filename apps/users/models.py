from django.db import models

# Create your models here.


class Vendor(models.Model):
    id = models.AutoField(primary_key=True)
    EmailID = models.EmailField()
    Username = models.CharField(max_length=200)
    person_id = models.CharField(max_length=200, null=True)
    Name = models.CharField(max_length=200, null=True)
    Dob = models.DateField('Dob', null=True)
    Designation = models.CharField(max_length=200, null=True)
    AadharCard = models.CharField(max_length=200, null=True)
    Address = models.CharField(max_length=500, null=True)
    PasswordReset = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Username
