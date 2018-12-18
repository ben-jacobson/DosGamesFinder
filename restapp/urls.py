from django.urls import path
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from dosgamesfinder import views

'''     # mimicking the Backbone routes
'publishers(/:page_number)': 'publishers_listview',
'genre/:genre(/:page_number)': 'filter_by_genre',
'publisher/:publisher(/:page_number)': 'filter_by_publisher',
'game/:request_slug': 'game', 
'(:page_number)': 'index',  
'''

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.HomeView.as_view(), name='home'),
    path('game/<slug:slug>', views.DosGameDetailView.as_view(), name='game'),

    # all api paths below to be removed 
    path('api/dosgames/', views.DosGameList.as_view(), name='DosGamesListView'),
    path('api/dosgames/<slug:slug>/', views.DosGameDetail.as_view(), name='DosGamesDetailView'),      

    path('api/publishers/', views.PublisherList.as_view(), name='PublisherListView'),
    path('api/publishers/<slug:slug>/', views.PublisherDetail.as_view(), name='PublisherDetailView'),      

    path('api/genres/', views.GenreList.as_view(), name='GenreListView'),
    path('api/genres/<slug:slug>/', views.GenreDetail.as_view(), name='GenreDetailView'),    
]

urlpatterns = format_suffix_patterns(urlpatterns)
