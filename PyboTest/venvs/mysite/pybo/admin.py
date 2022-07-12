import py_compile
from django.contrib import admin

#admin / admin / admin@admin.com

from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)
