from django.urls import path
from .views import result_list

urlpatterns = [
    path('', result_list, name='api_result_list'),
]
