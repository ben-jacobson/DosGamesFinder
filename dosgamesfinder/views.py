from django.views.generic import TemplateView
from dosgamesfinder.models import DosGame, Publisher, Genre
from dosgamesfinder.serializers import DosGameSerializer, PublisherSerializer, GenreSerializer
from rest_framework import generics
#from rest_framework.throttling import UserRateThrottle

class HomeView(TemplateView):
    template_name = "index.html"

class DosGameList(generics.ListAPIView):
    queryset = DosGame.objects.all()
    serializer_class = DosGameSerializer

class PublisherList(generics.ListAPIView):
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



