from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.Home.as_view(),name='home'),
    path('initializedb/', views.InitializeDB.as_view(), name='InitializeDB'),
    path('ajax/add_team/', views.Addteam.as_view(), name='Addteam'),
    path('ajax/match_win/', views.MatchWin.as_view(), name='match_win')
]