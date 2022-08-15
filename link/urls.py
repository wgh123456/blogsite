from django.urls import path
from . import views

urlpatterns = [
    path('add/',views.addLink,name='link-add'),
    path('update/',views.updateLink,name='link-update'),
]
