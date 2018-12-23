from django.urls import path
from django.contrib import admin
from dosgamesfinder import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots_file"),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="text/plain"), name="sitemap_file"),

    path('admin/', admin.site.urls),
    path('', views.DosGameListView.as_view(), name='dosgame_listview'),

    path('game/<slug:slug>', views.DosGameDetailView.as_view(), name='dosgame_detailview'),
    path('genre/<slug:slug>', views.DosGameListView.as_view(), name='genre_filter'),
    path('publisher/<slug:slug>', views.DosGameListView.as_view(), name='publisher_filter'),
    path('publishers/', views.PublisherListView.as_view(), name='publisher_listview'),    
]