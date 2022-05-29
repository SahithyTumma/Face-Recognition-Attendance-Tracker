# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
# Create your models here.


class UsersStudent(models.Model):
    id = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=200)
    Date = models.DateField('ON', null=True)
    In = models.TimeField("IN", null=True)
    Mealin = models.TimeField("Mealin", null=True)
    Mealout = models.TimeField("Mealout", null=True)
    Out = models.TimeField("Out", null=True)
    Vendor = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.Username

