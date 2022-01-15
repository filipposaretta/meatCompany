from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user_details/', views.user_details, name='user_details'),
    path('signup/', views.signup, name='signup'),
    path('lot_list/', views.lot_list, name='lot_list'),
    path('lot/<int:pk>/', views.lot_detail, name='lot_detail'),
    path('lot/<int:pk>/edit/', views.lot_edit, name='lot_edit'),
    path('lot/<pk>/remove/', views.lot_remove, name='lot_remove'),
    path('lot/new/', views.lot_new, name='lot_new'),
    path('lot_list/wrong_user/', views.wrong_user, name='wrong_user'),
    path('search/', views.search, name='search'),
    path('wallet/', views.wallet, name='wallet'),
]