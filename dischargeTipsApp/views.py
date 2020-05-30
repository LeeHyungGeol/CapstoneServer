from django.shortcuts import render
from konlpy.tag import Hannanum, Okt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import *


# Create your views here.

# sentence = [
        #     '아이스박스 어떻게 버려?',
        #     '전자레인지 버리는 방법 좀 알려줘']
        #
        # print()
        # for idx, val in enumerate(sentence):
        #     print(ha.nouns(val))
        # print()
# ['보온보냉팩', '방법']

class TextVoiceDischargeTipsView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, format=None): #JSON: "key" : "value" --> "searchWord" : "보온보냉팩 버리는 방법 좀 알려줘?"

        searchSentence = request.data['searchWord'] #안드로이드에서 searchWord 입력해야함
        if "캔" in searchSentence:
            print("Okt")
            okt = Okt()
            Nouns = okt.nouns(searchSentence)
        else:
            print("Hannanum")
            ha = Hannanum()
            Nouns = ha.nouns(searchSentence)
        print(Nouns)
        Idx = []
        temp = []
        for word in Nouns:
            smallIdx = WasteCategoryS.objects.filter(cg_name__contains = word)
            if not smallIdx:
                middleIdx = WasteCategoryM.objects.filter(cg_name__contains=word)
                for ob in middleIdx:
                    Idx.append(ob.idx)
                continue
            for ob in smallIdx:
                Idx.append(ob.cg_middle_idx.idx)
        Idx = list(set(Idx))
        print(Idx)
        dischargeTipsList = []
        for idx in Idx:
            dischargeTipsList.append(DischargeTips.objects.get(category_m_idx = idx))
        serializer = DischargeTipsSerializer(dischargeTipsList, many = True)
        
        return Response({
            "textVoiceDischargeTips": serializer.data
        },status=status.HTTP_201_CREATED)


class ImageDischargeTipsView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, format=None):  #JSON: "key" : "value" --> "cg_name" : "선풍기"
                                           # 이미지 품목 확인으로 나온 소분류 품목의 이름(cg_name)을 post의 형태로 받는다
        cg_name = request.data['cg_name']
        cg_middle_idx = WasteCategoryS.objects.get(cg_name = cg_name).cg_middle_idx
        dischargeTips = DischargeTips.objects.get(category_m_idx = cg_middle_idx.idx)
        serializer = DischargeTipsSerializer(dischargeTips)
        return Response({
            "imageDischargeTips" : serializer.data
        },status=status.HTTP_201_CREATED)




