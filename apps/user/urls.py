from django.urls import path
from apps.user import views

app_name = 'user'

urlpatterns = [
    # path('register', views.register, name='register'),  # 注册
    # path('register_handle', views.register_handle, name='register_handle'),  # 注册处理
    path('register', views.RegisterView.as_view(), name='register'),  # 注册
    path('active/<str:token>', views.ActiveView.as_view(), name='active'),  # 用户激活
    path('login', views.LoginView.as_view(), name='login'),  # 登录
    path('logout', views.LogoutView.as_view(), name='logout'),  # 注销

    path('', views.UserInfoView.as_view(), name='user'),  # 用户中心-信息页
    path('order', views.UserOrderView.as_view(), name='order'),  # 用户中心-订单页
    path('address', views.AddressView.as_view(), name='address'),  # 用户中心-地址页

]
