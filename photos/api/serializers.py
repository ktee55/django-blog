from rest_framework import serializers

from photos.models import Photo

class PhotoSerializer(serializers.ModelSerializer):

    thumbnail = serializers.ReadOnlyField(source="thumbnail.url")
    small = serializers.ReadOnlyField(source="small.url")
    medium = serializers.ReadOnlyField(source="medium.url")

    class Meta:
        model = Photo
        fields = ('id', 'origin', 'medium', 'small', 'thumbnail')
        # fields = '__all__'
