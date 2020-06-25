from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
from DetectionApp.detect import image_detect
from DetectionApp.models import *


# Create your views here.
class CommunityUserListAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, user_id):
        user = User.object.get(user_id= user_id)
        community_list = Community.objects.filter(user_idx = user).order_by('-date')
        # comments = PostingReviews.objects.filter(posting_idx = posting_idx)
        serializer = CommunityListSerializer(community_list, many=True)
        return Response({

            "community_list": serializer.data

        })


class CommunityListAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        community_list = Community.objects.all().order_by('-date')
        # comments = PostingReviews.objects.filter(posting_idx = posting_idx)
        serializer = CommunityListSerializer(community_list, many=True)
        return Response({

            "community_list": serializer.data

        })

    def post(self, request):
        user = request.user

        community = Community.objects.create(user_idx = user, share_complete = 0)
        serializer = CommunityDetailSerializer(community, data=request.data)
        if serializer.is_valid():
            serializer.save()
            img_url = serializer.data['image']
            results = image_detect('detection', img_url)

            if len(results) == 0:
                print('품목 인식 실패')
            else :
                s_list = list()
                for result in results:
                    print(result)
                    label = result['label']
                    accuracy = result['confidence']
                    try:
                        waste_s = WasteCategoryS.objects.get(label_name=label)
                        history = ItemdetectionSHistory.objects.create(user_idx=request.user, cg_idx=waste_s,
                                                                       accuracy=accuracy, image=img_url)
                        history.save()

                    except WasteCategoryS.DoesNotExist:
                        print("제공하지 않는 품목")

            return Response({
                "communitiy" : serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class CommunityDetailAPIView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self, idx):
        try:
            return Community.objects.get(idx=idx)
        except Community.DoesNotExist:
            raise Http404

    def get(self, request, idx, format=None):
        community = self.get_object(idx)
        print(community.user_idx.user_id)
        serializer = CommunityDetailSerializer(community)
        return Response({
            "community" : serializer.data
                         })

    def put(self, request, idx):
        community = self.get_object(idx)
        serializer = CommunityDetailSerializer(community, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "community": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, idx):
        community = self.get_object(idx)
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

