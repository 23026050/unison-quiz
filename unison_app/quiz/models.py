from django.db import models

# アルバムの情報を管理する
class Album(models.Model):
    title = models.CharField(max_length=200, verbose_name="アルバム名")
    release_date = models.DateField(null=True, blank=True, verbose_name="発売日")

    def __str__(self):
        return self.title

# 曲の情報を管理する（アルバムと紐付け）
class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs', verbose_name="収録アルバム")
    title = models.CharField(max_length=200, verbose_name="曲名")
    lyrics = models.TextField(verbose_name="歌詞")

    def __str__(self):
        return f"{self.album.title} - {self.title}"