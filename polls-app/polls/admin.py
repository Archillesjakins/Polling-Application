from django.contrib import admin
from .models import Question, Choice

# Register the Question model with the admin site
admin.site.register(Question)
admin.site.register(Choice)
