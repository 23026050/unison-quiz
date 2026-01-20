from django.db import models

class Question(models.Model):
    lyrics = models.TextField(verbose_name="歌詞")
    title = models.CharField(max_length=100, verbose_name="曲名（正解）")
    dummy_choice1 = models.CharField(max_length=100, verbose_name="ダミー選択肢1")
    dummy_choice2 = models.CharField(max_length=100, verbose_name="ダミー選択肢2")

    def __str__(self):
        return self.title