from django.urls import path
from apps.order import views

app_name = 'order'

urlpatterns = [
    path('place', views.OrderPlaceView.as_view(), name='place'),  # 提交订单页面显示
    path('commit', views.OrderCommitView.as_view(), name='commit'),  # 订单创建

]