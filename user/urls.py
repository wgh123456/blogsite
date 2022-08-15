from django.urls import path
from . import views

urlpatterns = [
    path('verify',views.verify_code,name="verify"), # 验证码
    path('login/',views.login_user,name='login'),
    path('register/',views.register_user,name='register'),
    path('logout/',views.logout_user,name='logout'),
    path('update/',views.update_user,name="user-update"),
]
