from django.urls import path
from apps.cart import views

app_name = 'cart'

urlpatterns = [
    path('add', views.CartAddView.as_view(), name='add'),  # 购物车记录的添加
    path('', views.CartInfoView.as_view(), name='show'),  # 购物车显示页面
    path('update', views.CartUpdateView.as_view(), name='update'),  # 购物车记录的更新
    path('delete', views.CartDeleteView.as_view(), name='delete'),  # 购物车记录的删除

]