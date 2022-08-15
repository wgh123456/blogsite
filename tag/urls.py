from django.urls import path,include
from . import views

urlpatterns = [
    path('add/',views.addTag,name='tag-add'),
    path('update/',views.updateTag,name='tag-update'),
]
