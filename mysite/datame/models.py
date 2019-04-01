from django.db import models
from django.contrib.auth.models import *
from django import forms
from django.utils import timezone
from django.template.defaultfilters import default

# Create your models here.

class Message(models.Model):
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    title = models.CharField('title', max_length = 100)
    body = models.TextField('body', max_length = 250)
    moment = models.DateTimeField(auto_now=True)
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

    def __str__(self):
        return self.name

class Offer(models.Model):
    CURRENCY_CHOICES = (
        ('0', '€'),
        ('1', '$'),
        ('2', '£')
    )


    title = models.CharField('Offer title', max_length = 80)
    description = models.TextField('Offer description')
    price_offered = models.FloatField('Price offered')
    currency = models.CharField('Currency type',max_length = 1, choices = CURRENCY_CHOICES)
    creation_date = models.DateTimeField(auto_now_add=True)
    limit_time = models.DateTimeField(blank=True)
    finished = models.BooleanField(default=False)
    files = models.URLField()
    contract = models.TextField('Contract')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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
    description = models.CharField("Description", max_length=100)
    entity = models.CharField("Entity", max_length=50)
    date_start = models.DateTimeField("Start date")
    date_finish = models.DateTimeField("End date", blank=True, null=True)

    def __str__(self):
        return self.name
