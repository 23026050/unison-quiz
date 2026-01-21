from django.contrib import admin
from django.urls import path
from quiz.views import quiz_view, check_answer ,reset_quiz # 使うのはこの2つだけ！

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', quiz_view, name='quiz'),
    path('check/', check_answer, name='check_answer'),
    path('reset/', reset_quiz, name='reset_quiz'),
]