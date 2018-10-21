from django.views.generic import TemplateView
from dosgamesfinder.models import DosGame
from dosgamesfinder.serializers import DosGameSerializer
from rest_framework import generics
from rest_framework.throttling import UserRateThrottle

class HomeView(TemplateView):
    template_name = "index.html"

class DosGameList(generics.ListAPIView):
    throttle_classes = (UserRateThrottle,)
    queryset = DosGame.objects.all()
    serializer_class = DosGameSerializer

class DosGameDetail(generics.ListAPIView):
    throttle_classes = (UserRateThrottle,)
    queryset = DosGame.objects.all()
    serializer_class = DosGameSerializer