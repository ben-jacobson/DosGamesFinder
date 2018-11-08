from django.views.generic import TemplateView
from dosgamesfinder.models import DosGame, Publisher, Genre
from dosgamesfinder.serializers import DosGameSerializer, PublisherSerializer, GenreSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
#from rest_framework.throttling import UserRateThrottle

# our pagination mixin classes - This is how you cusomize the page_sizes for pagination styles

class DosGamesPageNumberPagination(PageNumberPagination):
    page_size = 18
    max_page_size = page_size
    #page_size_query_param = 'page_size'    

class PublisherPageNumberPagination(PageNumberPagination):
    page_size = 10
    max_page_size = page_size

# our views

class HomeView(TemplateView):
    template_name = "index.html"

class DosGameList(generics.ListAPIView):
    pagination_class = DosGamesPageNumberPagination     # see how you can set pagination styles,    
    queryset = DosGame.objects.all()
    serializer_class = DosGameSerializer

class PublisherList(generics.ListAPIView):
    pagination_class = PublisherPageNumberPagination
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class GenreList(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

# Detail Views

class DosGameDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = DosGame.objects.all()        # I was skeptical too of using objects.all() but I can see in 3 separate posts that this is the correct way to do it..
    serializer_class = DosGameSerializer

class PublisherDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer    

class GenreDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer



