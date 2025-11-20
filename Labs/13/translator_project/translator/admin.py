from django.contrib import admin
from .models import Dictionary

@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ['english_word', 'russian_translation', 'created_at']
    list_filter = ['created_at']
    search_fields = ['english_word', 'russian_translation']
    ordering = ['english_word']