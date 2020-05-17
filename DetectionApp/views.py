from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from rest_framework import status
from django.http import Http404
from rest_framework import permissions

from .serializers import *
from .models import *
from .darkflow import ImageDetection

# Create your views here.
class CleanDetectionAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):

        try:
            history = PointHistory.objects.filter(user_idx = request.user).order_by('-date')
            recent_date = history[0].date
            cool_time = timezone.now() - recent_date
            if cool_time.days < 1:
                return Response({
                    "clean_detection": "하루에 한번만 가능합니다."
                })

        except IndexError :
            upload_serializer = UploadSerializer(data= request.data)

            if upload_serializer.is_valid():
                upload_serializer.save()
                img_url = upload_serializer.data['image']
                results = ImageDetection.getItemName(img_url)
                print(results)

                if len(results) == 0 :
                    return Response({
                        "clean_detection" : "품목 분류에 실패했습니다."
                    })

                label = results[0]['label']
                accuracy = results[0]['confidence']
                print(label,accuracy)
                if label == 'labelRemovalPetBottle' or label == 'CompressedCan' or label == 'StackedBox' or 'Kongguksu':
                    clean_waste = WasteCategoryS.objects.get(label_name=label)
                    history = PointHistory.objects.create(user_idx = request.user, value = 100, point_description = clean_waste)
                    history.save()
                    serializer = PointHistorySerializer(history)
                    return Response({

                        "clean_detection" : serializer.data
                                     }, status = status.HTTP_201_CREATED)
                return Response({
                    "clean_detection": "깨끗한 상태가 아닙니다."
                })

            return Response(upload_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DetectionAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):

        upload_serializer = UploadSerializer(data= request.data)

        if upload_serializer.is_valid():
            upload_serializer.save()
            img_url = upload_serializer.data['image']
            results = ImageDetection.getItemName(img_url)
            print(results)
            if len(results) == 0 :
                return Response({
                    "detection_list" : "품목 분류에 실패했습니다."
                })

            s_list = list()

            for result in results:
                print(result)
                label = result['label']
                accuracy = result['confidence']
                try:
                    waste_s = WasteCategoryS.objects.get(label_name =label)
                    history = ItemdetectionSHistory.objects.create(user_idx = request.user, cg_idx = waste_s, accuracy= accuracy, image= img_url)
                    history.save()
                    s_list.append(waste_s)

                except WasteCategoryS.DoesNotExist:
                    print("제공하지 않는 품목")

            s_serializer = WasteCategorySSerializer(s_list, many=True)
            return Response({
                "detection_list" : s_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(upload_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
