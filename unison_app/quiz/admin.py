from django.contrib import admin
from .models import Album, Song

# 管理画面でアルバムと曲を登録できるようにする
admin.site.register(Album)
admin.site.register(Song)