from django.contrib import admin
from .models import Word, LearnedWord, Dict, QuickCard

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'translation', 'transcription')
    search_fields = ('word', 'translation')

@admin.register(LearnedWord)
class LearnedWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'learned_at')
    search_fields = ('word__word',)

@admin.register(Dict)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'word_eng', 'transcription', 'pos', 'translation')
    search_fields = ('word', 'translation')

@admin.register(QuickCard)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'word')
    search_fields = ('word', 'user')

