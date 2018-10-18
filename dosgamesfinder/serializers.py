from rest_framework import serializers
from dosgamesfinder.models import DosGame

class DosGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DosGame
        # for now, we'll want all fields, will narrow this down later.
        fields = '__all__'
