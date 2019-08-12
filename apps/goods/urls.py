from django.urls import path
from apps.goods import views

app_name = 'goods'

urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),  # 首页
    path('goods/<int:goods_id>', views.DetailView.as_view(), name='detail'),  # 商品详情页
    path('list/<int:type_id>/<int:page>', views.ListView.as_view(), name='list'),  # 列表页
    path('', views.IndexView.as_view(), name='index'),  # 列表页

]