from django.urls import path
from . import views


urlpatterns = [
    path('',views.FrontIndexView.as_view(),name='front-index'),
    path('read/',views.ReadArticleView.as_view(),name='front-read'),
    path('links/<str:group>/',views.LinkGroupArticleView.as_view(),name='front-link-group'),
    path('tags/<str:group>/',views.TagGroupArticleView.as_view(),name='front-tag-group'),
    path('search/<str:group>/',views.SearchArticleView.as_view(),name='front-search-group'),
]
