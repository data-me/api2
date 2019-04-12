from django.db import models
from django.contrib.auth.models import *
from django import forms
from django.utils import timezone
from django.template.defaultfilters import default
from django.db.models.fields.related import OneToOneField

# Create your models here.

class Message(models.Model):
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    title = models.CharField('title', max_length = 100)
    body = models.TextField('body', max_length = 250)
    moment = models.DateTimeField(auto_now=True)
    isAlert = models.BooleanField(default=False)
    def __str__(self):
        return self.title


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length = 30)
    description = models.TextField('Description', max_length = 50)
    nif = models.CharField('NIF', max_length = 9)
    logo = models.URLField('Logo URL')

    def __str__(self):
        return self.name


class DataScientist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length = 30)
    surname = models.CharField('Surname', max_length = 50)
    email = models.EmailField('Email')
    photo = models.CharField('Photo', max_length = 100)
    address = models.CharField('Address', max_length = 100)
    phone = models.CharField('Phone', max_length = 9)

    def __str__(self):
        return self.name
    
class UserPlan(models.Model):
    
    TYPE_CHOICES = (
        ('PRO', 'PRO'),
    )
    
    dataScientist = models.ForeignKey(DataScientist, on_delete=models.CASCADE)
    type = models.CharField('Type', max_length = 4, choices = TYPE_CHOICES)
    startDate = models.DateTimeField(null = True)
    expirationDate = models.DateTimeField(null = True)
    isPayed = models.BooleanField(default= False)

    def __str__(self):
        res = 'User Plan from ' + self.dataScientist.name
        return res

class Offer(models.Model):


    title = models.CharField('Offer title', max_length = 80)
    description = models.TextField('Offer description')
    price_offered = models.FloatField('Price offered')
    creation_date = models.DateTimeField(auto_now_add=True)
    limit_time = models.DateTimeField(blank=True)
    finished = models.BooleanField(default=False)
    files = models.URLField()
    contract = models.TextField('Contract')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Submition(models.Model):
    
    STATUS_CHOICES = (
        ('SU', 'SUBMITTED'),
        ('AC', 'ACEPTED'),
        ('RE', 'REJECTED')
    )
    
    dataScientist = models.ForeignKey(DataScientist, on_delete=models.CASCADE)
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE,)
    file = models.CharField('File', max_length = 100)
    comments = models.CharField('Comments', max_length = 100)
    status = models.CharField('Status', max_length = 9, choices = STATUS_CHOICES)
    

    def __str__(self):
        res = 'Submition ' + self.offer.title + ' from ' + self.dataScientist.name
        return res

class Apply(models.Model):

    STATUS_CHOICES = (
        ('PE', 'PENDING'),
        ('AC', 'ACEPTED'),
        ('RE', 'REJECTED')
    )

    title = models.CharField('Apply title', max_length = 80)
    description = models.TextField('Apply description')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField('Status',max_length = 8, choices = STATUS_CHOICES)
    dataScientist = models.ForeignKey(DataScientist, default="",on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

# Curriculum vitae
class CV(models.Model):
    owner = models.OneToOneField('datame.DataScientist', default = "", on_delete = models.CASCADE)

    def __str__(self):
        return self.owner.name

class Section_name(models.Model):
    name = models.CharField("Name", max_length=50)

    def __str__(self):
        return self.name

# Sections of a curriculum
class Section(models.Model):
    name = models.ForeignKey("datame.Section_name", on_delete = models.CASCADE, related_name = 'section_name')
    cv = models.ForeignKey("datame.CV", on_delete = models.CASCADE, related_name = 'sections')

    def __str__(self):
        return self.name.name

# Items of a section
class Item(models.Model):
    name = models.CharField("Name", max_length=50)
    section = models.ForeignKey("datame.Section", on_delete = models.CASCADE, related_name = 'items')
    description = models.CharField("Description", max_length=500)
    entity = models.CharField("Entity", max_length=50, blank=True,null=True)
    date_start = models.DateField("Start date")
    date_finish = models.DateField("End date", blank=True, null=True)

    def __str__(self):
        return self.name
