from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
from .ar_markers.bin import ar_markers_generate
from .object_size import length_measure

# Create your views here.
class MarkerAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]


    def get(self, request, format=None):

        url = ar_markers_generate.generate_marker()
        return Response({
            "marker " : url
        })


class MeasureAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]


    def post(self, request, format=None):

        upload_serializer = MeasureUploadSerializer(data= request.data)

        if upload_serializer.is_valid():
            upload_serializer.save()
            img_url = upload_serializer.data['image']
            url_list = length_measure(img_url)
            upload_list = list()
            for url in url_list:
                upload_list.append(Upload.objects.create(image = url))
            serializer = MeasureUploadSerializer(upload_list, many=True)
            return Response({
                "measure" :serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(upload_serializer.errors, status=status.HTTP_400_BAD_REQUEST)