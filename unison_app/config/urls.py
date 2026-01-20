from django.contrib import admin
from django.urls import path
from quiz.views import quiz_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', quiz_view, name='quiz'),
]