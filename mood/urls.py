from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_mood, name='add_mood'),
    
    # 刪除功能需要知道是哪一筆資料，所以網址帶有 <int:pk> (資料的 ID 編號)
    path('delete/<int:pk>/', views.delete_mood, name='delete_mood'),
    
    # 圖表統計的網址
    path('statistics/', views.statistics, name='statistics'),
    # --- 會員系統網址 ---
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/moods/', views.mood_api, name='mood_api'),
]