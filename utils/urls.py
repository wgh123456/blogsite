from django.urls import path,include
from . import views


urlpatterns = [
    path('emailcheckcode/',views.emailcheckcode,name='emailcheckcode'),
    path('uploadfile/',views.uploadfile,name='uploadfile'),
]