from django.conf.urls import url
from django.urls import path, include
from .views import (
    MemeListApiView,
    MemeDetailApiView
)

urlpatterns = [
    path('meme', MemeListApiView.as_view()),
    path('meme/<int:meme_id>/', MemeDetailApiView.as_view()),
]
