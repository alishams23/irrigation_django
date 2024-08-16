from django.shortcuts import render
from rest_framework import generics
from .models import Video
from .serializers import VideoSerializer
from rest_framework.permissions import AllowAny
# Create your views here.


class VideoListAPIView(generics.ListAPIView):    
    permission_classes = (AllowAny, )
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    