from django.urls import path
from apps.goods import views

app_name = 'goods'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # 首页

]