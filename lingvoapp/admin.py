from django.contrib import admin
from .models import Material,Dictionary,DictionaryInverted,Question,AnswerOptions
# Register your models here.
admin.site.register(Material)
admin.site.register(Dictionary)
admin.site.register(DictionaryInverted)
admin.site.register(Question)
admin.site.register(AnswerOptions)