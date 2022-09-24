from pyexpat import model
from statistics import mode
from typing import MutableSequence
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import AutoField, CharField
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings


class Student(models.Model):
    table_id = models.AutoField(primary_key=True)
    user_type = models.IntegerField(default=0)
    username=models.CharField(max_length=100,null=True)
    name = models.CharField(max_length=50,default="")
    age = models.IntegerField(default=0)
    area =models.CharField(max_length=100,default ="")
    state=models.CharField(max_length=100,default ="")
    email = models.EmailField(max_length=254,default="")
    phone=models.CharField(max_length=20,default ="")
    college=models.CharField(max_length=100,default ="")
    course=models.CharField(max_length=100,default ="")
    description=models.CharField(max_length=1000,default ="")
    completion_status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Investor(models.Model):
    table_id = models.AutoField(primary_key=True)
    user_type = models.IntegerField(default=0)
    username=models.CharField(max_length=100,null=True)
    name = models.CharField(max_length=50,default="")
    phone = models.CharField(max_length=20,default ="")
    description=models.CharField(max_length=1000,default ="")
    linkedln = models.CharField(max_length=30,default="")
    email = models.EmailField(max_length=254,default="")
    completion_status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Startup(models.Model):
    startup_id=models.AutoField(primary_key=True)
    user_type=models.IntegerField(default=0)
    username=models.CharField(max_length=100,null=True)
    name=models.CharField(max_length=50,default="")
    tagname=models.CharField(max_length=200,default="")
    about=models.CharField(max_length=2000,default="")
    comapany_type=models.CharField(max_length=50,default="")
    market_cap=models.IntegerField(default=0)
    netsales=models.IntegerField(default=0)
    revenue=models.IntegerField(default=0)
    profit_after_tax=models.IntegerField(default=0)
    profit_growth=models.IntegerField(default=0)
    company_mission=models.CharField(max_length=2000,default=0)
    fund_to_be_raised=models.IntegerField(default=0)
    hiring_details=models.CharField(max_length=2000,default="")
    job_vacancy=models.IntegerField(default=0)
    website_link=models.CharField(max_length=100,default=0)
    email = models.EmailField(max_length=254,default="")
    linkedin_link=models.CharField(max_length=100,default=0)
    twitter_link=models.CharField(max_length=100,default=0)
    completion_status=models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Request(models.Model):
    table_id = models.AutoField(primary_key=True)
    user_name = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    startup_name=models.ForeignKey(Startup,on_delete=models.CASCADE)
    user_type = models.IntegerField(default=0)
    request_type = models.IntegerField(default=0)
    description=models.CharField(max_length=1000,default ="")
    specific_link=models.CharField(max_length=200,default=0)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.IntegerField(default=0)

    def _str_(self):
        return str(self.user_name)
