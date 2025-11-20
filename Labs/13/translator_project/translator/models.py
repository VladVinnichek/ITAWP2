from django.db import models

class Dictionary(models.Model):
    english_word = models.CharField(max_length=100, verbose_name="Английское слово", unique=True)
    russian_translation = models.CharField(max_length=100, verbose_name="Русский перевод")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    def __str__(self):
        return f"{self.english_word} - {self.russian_translation}"
    
    class Meta:
        verbose_name = "Слово в словаре"
        verbose_name_plural = "Словарь"
        ordering = ['english_word']