from unicodedata import name
from django.urls import path
from . import views
from .views import AdminIndexView,AdminUserxView,AdminArticleView,AdminTagView,AdminLinkView,AdminCarouselView



urlpatterns = [
    path('',AdminIndexView.as_view(),name='admin-index'),
    path('user/',AdminUserxView.as_view(),name='admin-user'),
    path('article/',AdminArticleView.as_view(),name='admin-article'),
    path('tag/',AdminTagView.as_view(),name='admin-tag'),
    path('link/',AdminLinkView.as_view(),name='admin-link'),
    path('carousel/',AdminCarouselView.as_view(),name='admin-carousel')

    # path('image/upload/',AdminImageView.as_view(),name='image-upload'),
    # path('image/cover/',CoverUploadView.as_view(),name='cover-upload'),
    # path('write/',AdminWriteView.as_view(),name='write'),
]
