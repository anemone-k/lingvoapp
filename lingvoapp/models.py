from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Material(models.Model):
    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")
        ordering = ['id']
    name = models.CharField(max_length=70, blank=False, default='')
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False,default='')


class Dictionary(models.Model):
    class Meta:
        verbose_name = _("DictionaryWord")
        verbose_name_plural = _("DictionaryWords")
        ordering = ['id']
    word = models.TextField( blank=False, default='',unique=True)

    translation = models.TextField( blank=False, default='')
    state = models.IntegerField(default=0)
    edited = models.DateTimeField(auto_now=True)


class DictionaryInverted(models.Model):
    class Meta:
        verbose_name = _("DictionaryInvertedWord")
        verbose_name_plural = _("DictionaryInvertedWords")
        ordering = ['id']
    word = models.TextField(blank=False, default='',unique=True)

    translation = models.TextField(blank=False, default='')
    state = models.IntegerField(default=0)
    edited = models.DateTimeField(auto_now=True)


class Question(models.Model):

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['id']

    questionText = models.CharField(max_length=255, verbose_name=_("Title"))
    dateCreated = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Date Created"))

    def __str__(self):
        return self.questionText


class AnswerOptions(models.Model):

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ['id']

    question = models.ForeignKey(
        Question, related_name='answer', on_delete=models.CASCADE)
    answerText = models.CharField(
        max_length=255, verbose_name=_("Answer Text"))
    wordId=models.IntegerField(default=0)
    isCorrect = models.BooleanField(default=False)

    def __str__(self):
        return self.answerText




