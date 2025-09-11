from django.db import models
from django.contrib.auth.models import User



class Dict(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    word_eng = models.CharField(max_length=255, db_column='word')
    transcription = models.CharField(max_length=255, blank=True, null=True, db_column='transcription')
    pos = models.CharField(max_length=255, db_column='pos')
    translation = models.CharField(max_length=255, blank=True, null=True, db_column='translation')

    class Meta:
        db_table = 'dict'
        managed = False  # Django не будет менять эту таблицу

    def __str__(self):
        return self.word_eng

class Word(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    word = models.CharField(max_length=255, db_column='word')
    part_of_speech = models.CharField(max_length=255, db_column='part_of_speech')
    level = models.CharField(max_length=255, db_column='level')
    translation = models.CharField(max_length=255, db_column='translation')
    transcription = models.CharField(max_length=255, blank=True, null=True, db_column='transcription')
    definition_examples = models.TextField(blank=True, null=True, db_column='definition_examples')

    class Meta:
        db_table = 'words'
        managed = False  # Django не будет менять эту таблицу

    def __str__(self):
        return self.word


# Таблица для выученных слов
class LearnedWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_words')
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    learned_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.word.word} (выучено)"


class QuickCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_quick_card')
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    translation = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.word.word}"