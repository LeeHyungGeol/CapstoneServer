from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
from .ar_markers.bin import ar_markers_generate
from .object_size import measure_length
from DetectionApp.models import WasteCategoryS, CategoryRegulation
import math
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
            result_list = measure_length(img_url, request.user)

            if result_list is False:
                msg = "마커 인식에 실패했습니다."
                return Response({
                    "measure": {"code": 101,
                                        "msg" : msg}
                })
            elif len(result_list) == 0:
                msg = "길이 측정에 실패했습니다."
                return Response({
                    "measure": {"code": 102,
                                        "msg" : msg}
                })
            else :

                serializer = MeasureHistorySerializer(result_list, many=True)
                return Response({
                    "measure" :serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response(upload_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchFeeAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]


    def post(self, request, format=None):

        match_serializer =MatchFeeSerializer(data = request.data)
        if match_serializer.is_valid():
            cg_name = match_serializer.data['cg_name']
            width = match_serializer.data['width']
            height = match_serializer.data['height']

            try:
                waste = WasteCategoryS.objects.filter(cg_name__contains = cg_name)
                item = RegulationFee.objects.filter(cg_idx = waste[0])

            except Exception:

                msg = "품목명 잘못 입력 또는 길이에 따른 수수료가 없는 품목입니다."
                return Response({
                    "fee": {"code": 101,
                            "msg": msg}
                })

            else :
                fee = 0
                for val in item:
                    if val.fee_flag == 'width':
                        print('width')
                        condition = width
                    elif val.fee_flag == 'height':
                        print('height')
                        condition = height
                    elif val.fee_flag == 'both':
                        print('both')
                        if width > height:
                            condition = width
                        else :
                            condition = height
                    elif val.fee_flag == 'triangle':
                        print('triangle')
                        inch = math.sqrt(math.pow(width,2) + math.pow(height,2))
                        condition = inch

                    else :
                        print('wrong flag')
                        raise Http404

                    if val.condition_value <= condition:
                        print(val.over_fee)
                        fee = val.over_fee
                        break

                    else:
                        if val.down_fee != 'more':
                            print(val.down_fee)
                            fee = val.down_fee
                            break
                        else:
                            continue

                return Response({
                    'fee': {
                        'item_fee' : fee,
                        'code' : 100,
                        'msg' : '성공'
                    }
                })


        return Response(match_serializer.errors, status=status.HTTP_400_BAD_REQUEST)