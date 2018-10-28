from django.urls import path
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from dosgamesfinder import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),

    path('api/dosgames/', views.DosGameList.as_view(), name='DosGamesListView'),
    path('api/dosgames/<slug:slug>/', views.DosGameDetail.as_view(), name='DosGamesDetailView'),      

    path('api/publishers/', views.PublisherList.as_view(), name='PublisherListView'),
    path('api/publishers/<slug:slug>/', views.PublisherDetail.as_view(), name='PublisherDetailView'),      

    path('api/genres/', views.GenreList.as_view(), name='GenreListView'),
    path('api/genres/<slug:slug>/', views.GenreDetail.as_view(), name='GenreDetailView'),    
]

urlpatterns = format_suffix_patterns(urlpatterns)
