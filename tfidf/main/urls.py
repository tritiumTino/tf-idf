from django.urls import path
from .views import index, file_to_analysis


app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('analisys/<int:id>/', file_to_analysis, name='file_to_analysis')
]
