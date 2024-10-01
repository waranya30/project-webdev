from django.contrib import admin
from django.urls import path, include
from menu import views
from django.contrib.auth import views as auth_views
from .views import delete_menu, edit_menu
from .views import CustomLoginView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.order_and_reserve, name='order_and_reserve'),
    path('home/', views.home, name='home'),
    path('order/', views.order_food, name='order_food'),
    path('login/', views.login_view, name='custom_login'),  # เปลี่ยนชื่อเส้นทางให้ไม่ซ้ำกับ 'auth_views.LoginView'
    path('signup/', views.signup, name='signup'),  # เส้นทางสำหรับการสมัครสมาชิก
    path('add/', views.add_menu, name='add_menu'),
    path('menus/', views.menu_list, name='menu_list'),
    path('edit/<int:menu_id>/', edit_menu, name='edit_menu'),
    path('delete/<int:menu_id>/', delete_menu, name='delete_menu'),
    path('my-sales/', views.my_sales, name='my_sales'),
    path('profile/', views.profile, name='profile'),  # เพิ่มลิงก์โปรไฟล์ที่นี่
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # หน้าแก้ไขโปรไฟล์
    # ใช้เส้นทางเข้าสู่ระบบ/ออกจากระบบและจัดการรหัสผ่านที่มากับ auth_views ของ Django
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='custom_login'), name='logout'),  # เปลี่ยน 'home' เป็น 'custom_login'
    path('accounts/login/', CustomLoginView.as_view(next_page='home'), name='login'),
    path('order-and-reserve/', views.order_and_reserve, name='order_and_reserve'),
    path('reserve/', views.reserve_table, name='reserve_table'),
    path('reservation/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),  # เพิ่มเส้นทางสำหรับหน้ารายละเอียดการจอง
   
]
