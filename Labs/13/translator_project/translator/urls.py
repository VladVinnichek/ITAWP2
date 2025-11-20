from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('translate/', views.translate_word, name='translate'),
    path('add-word/', views.add_word, name='add_word'),
]