from django.db import models

# Create your models here.


class Material(models.Model):
    name = models.CharField(max_length=70, blank=False, default='')
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False,default='')


class Dictionary(models.Model):
    word = models.CharField(max_length=200, blank=False, default='',unique=True)
    translation = models.CharField(max_length=200, blank=False, default='')
    state = models.IntegerField(default=0)
    edited = models.DateTimeField(auto_now=True)


class DictionaryInverted(models.Model):
    word = models.CharField(max_length=200, blank=False, default='',unique=True)
    translation = models.CharField(max_length=200, blank=False, default='')
    state = models.IntegerField(default=0)
    edited = models.DateTimeField(auto_now=True)



