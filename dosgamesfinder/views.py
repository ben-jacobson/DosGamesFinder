from django.views.generic import TemplateView
from dosgamesfinder.models import DosGame
from dosgamesfinder.serializers import DosGameSerializer
from rest_framework import generics

class HomeView(TemplateView):
    template_name = "index.html"

class DosGameList(generics.ListCreateAPIView):
    queryset = DosGame.objects.all()
    serializer_class = DosGameSerializer

class DosGameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DosGame.objects.all()
    serializer_class = DosGameSerializer