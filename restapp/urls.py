from django.urls import path
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from dosgamesfinder import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('api/dosgames/', views.DosGameList.as_view(), name='DosGamesListView'),
    path('api/dosgames/<int:pk>/', views.DosGameDetail.as_view(), name='DosGamesDetailView'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
