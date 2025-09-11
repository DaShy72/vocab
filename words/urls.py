from django.urls import path
from . import views

app_name = 'words'

urlpatterns = [
    path('', views.word_list, name='word_list'),
    path('<int:pk>/', views.word_detail, name='word_detail'),
    path('random/', views.random_word, name='random_word'),
    path('learned/', views.learned_list, name='learned_list'),
    path('quick_card', views.quick_card, name='quick_card'),
    path('fill_up_card/<int:pk>', views.fill_up_card, name='fill_up_card'),
    path('statistics', views.statistics, name='statistics'),
    path('dictionary', views.dictionary, name='dictionary'),
]
