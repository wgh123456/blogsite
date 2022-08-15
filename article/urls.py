from django.urls import path,include
from .views import AdminWriteView,UpdateArticleView,CarouseEditlView,UpdateCarouselView,DeleteArticleView

urlpatterns = [
    # 上传封面
    path('write/',AdminWriteView.as_view(),name='write'),
    path('update/',UpdateArticleView.as_view(),name='update'),
    path('delete/',DeleteArticleView.as_view(),name='delete'),
    # 上传轮播图
    path('carouseledit/',CarouseEditlView.as_view(),name='carousel-edit'),
    path('carouselupdate/',UpdateCarouselView.as_view(),name='carousel-update'),
]
