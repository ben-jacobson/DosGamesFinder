from rest_framework import serializers
from dosgamesfinder.models import Publisher, DosGame, Screenshot, DownloadLocation

class DownloadLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadLocation
        exclude = ('id', 'game', ) # if you use exclude, you don't need the fields = '__all__' as above 

class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        exclude = ('id', 'game', )   

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'        

class DosGameSerializer(serializers.ModelSerializer):
    # in order to serialize nested relationships, we nest them here. 
    screenshots = ScreenshotSerializer(many=True, read_only=True)
    download_locations = DownloadLocationSerializer(many=True, read_only=True)
    publisher = PublisherSerializer(many=False, read_only=True)

    class Meta:
        model = DosGame
        fields = '__all__'        
        #depth = 1          # With this, you can set the depth of how many Foreign keys you wish your serializer to traverse. 
                            # With a depth of zero (default), it will simply list the primary key of the related field
                            # With a depth of 1 or more, it will automatically traverse the primary keys and serialize their data too.
                            # In this models case, we need to serialize the publisher foreign keys and also the related screenshots and download locations, so have done this manually to maintain control over the serializer behaviour