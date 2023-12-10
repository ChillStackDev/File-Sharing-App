from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name="index"),
    path('logout/',logout_page,name="logout"),
    path('login/',login_page,name="login"),
    path('register/',register,name="register"),
    path('search/', search, name='search'),
    path('share_file/<int:file_id>/', share_file, name='share_file'),
   
    path('download/<int:file_id>/', download_file, name='download_file'),

]
