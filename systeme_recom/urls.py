from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index,name='index'),
    path('recom',views.recom, name='recom'),
    path('culture',views.culture, name='culture'),
    path('contact',views.contact, name='contact'),
    path('apropos',views.apropos, name='apropos'),
    path('mil',views.mil, name='mil'),
    path('riz',views.riz, name='riz'),
    path('arahide',views.arachide, name='arachide'),
    path('mais',views.mais, name='mais'),
    path('sorgho',views.sorgho, name='sorgho'),
    path('tomate',views.tomate, name='tomate'),
    path('niebe',views.niebe, name='niebe'),
    path("register", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("profil", views.profil, name="profil"),
    path("search", views.search, name="search"),
    path("dashboard", views.dashboard, name="dashboard"),


]
