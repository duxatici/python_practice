from rest_framework import serializers

from .models import Video, VideoFile


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ("video", "file", "quality")


class VideoSerializer(serializers.ModelSerializer):
    files = VideoFileSerializer(many=True)
    owner = serializers.CharField(source="owner.username")

    class Meta:
        model = Video
        fields = ("owner", "is_published", "name", "total_likes", "created_at", "files")
