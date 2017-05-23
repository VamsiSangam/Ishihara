from django.contrib import admin
from app.models import *

# Register your models here.
class VisionCaseAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'image',)
    search_fields = ['text', 'image']

class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'option', 'case')
    search_fields = ['question', 'case']
    list_filter = ('case',)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'option')
    search_fields = ['user', 'question', 'option']
    
admin.site.register(VisionCase, VisionCaseAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Answer, AnswerAdmin)