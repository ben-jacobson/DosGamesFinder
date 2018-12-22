from django.urls import path
from django.contrib import admin
from dosgamesfinder import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.DosGameListView.as_view(), name='dosgame_listview'),
    path('game/<slug:slug>', views.DosGameDetailView.as_view(), name='dosgame_detailview'),
    path('genre/<slug:slug>', views.DosGameListView.as_view(), name='genre_filter'),
    path('publisher/<slug:slug>', views.DosGameListView.as_view(), name='publisher_filter'),
    path('publishers/', views.PublisherListView.as_view(), name='publisher_listview'),    
]