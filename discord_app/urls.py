from django.urls import path
from . import views
urlpatterns = [
    path("login/",views.login_page,name="login"),
    path("logout/",views.lougout_user,name="logout"),
    path("register/",views.register_page,name="register"),


    path("",views.home,name="home"),
    path("room/<str:pk>/",views.room,name="room"),
    path("create_room",views.create_room,name="create_room"),
    path("edit_room/<str:pk>",views.edit_room,name="edit_room"),
    path("delete_room/<str:pk>",views.delete_room,name="delete_room"),
    path("delete_message/<str:pk>",views.delete_message,name="delete_message")
]