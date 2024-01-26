from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
class QuestionAdmin(admin.ModelAdmin):
    
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    # admin上でフィールドを分割し、見やすくする
    fieldsets = [
        ("Text", {"fields": ["question_text"]}),
        ("Data information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    
    inlines = [ChoiceInline]
    
admin.site.register(Question, QuestionAdmin)
