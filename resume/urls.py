from django.urls import path
from .views import Extract


urlpatterns = [ 
             path('home/', Extract, name='homepage'), 
      ]
