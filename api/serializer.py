from rest_framework import serializers
from .models import TblCreator,Video,tblcomment


class TblCreatorSerializer(serializers.ModelSerializer):
    class Meta:
     model = TblCreator
     fields = '__all__'
     
     
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'  # includes video_file

class tblcommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = tblcomment
        fields = '__all__'  # includes video_file
 