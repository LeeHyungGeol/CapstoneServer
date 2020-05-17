from django.shortcuts import render
from rest_framework import permissions, generics, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from knox.models import AuthToken
from .serializers import *
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import TokenAuthentication
from django.contrib.auth import login
from rest_framework.views import APIView

# Create your views here.
@api_view(["GET"])
def HelloAPI(request):

    print(request.user)
    return Response("hello world!")


class RegistrationAPI(generics.GenericAPIView):
    renderer_classes = [JSONRenderer]

    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        # if len(request.data["user_id"]) < 6 or len(request.data["password"]) < 4:
        #     body = {"message": "short field"}
        #     return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(generics.GenericAPIView):
    renderer_classes = [JSONRenderer]
    # 토큰인증은 username, password로 로그인 인증을 하는데
    # username : 가입 시 name 이므로 email 주소이다.. 씨발;
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            "user_id": UserSerializer(user,
                                   context=self.get_serializer_context()).data['user_id'],
            "token": AuthToken.objects.create(user)[1]
        })


class UserAPI(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UserSerializer

    def get_object(self):
        # print(self.request.auth)
        # print(self.request.data)
        # print(self.request.user.idx)
        # print(self.request.content_type)
        # print(self.request.FILES)
        # print(self.request.user.user_email)
        # print(self.request.user.idx)
        # print(self.request.user.user_id)

        return self.request.user


class UserProfileView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({
           "my_page": serializer.data
        })

    def put(self, request, format=None):
        serializer = UpdateUserProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "update_my_page" : serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserShareListView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, format=None):
        user = request.user
        community_information = Community.objects.filter(user_idx = user)
        serializer = UserShareCompleteCheckSerializer(community_information, many=True)
        return Response({
           "community": serializer.data
        })


class UserShareCompleteCheckView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, idx, format=None):  #community 테이블의 번호를 넘겨줘야 함
        user = request.user
        community_information = Community.objects.get(idx = idx, user_idx = user)
        print(community_information.share_complete)
        if community_information.share_complete == 0:
            community_information.share_complete = 1
            print(community_information.share_complete)
            community_information.save()
            serializer = UserShareCompleteCheckSerializer(community_information)
            msg = "나눔 완료!"
            return Response({
                    "msg": msg,
                    "community": serializer.data
                })
        else:
            community_information.share_complete = 0
            print(community_information.share_complete)
            community_information.save()
            serializer = UserShareCompleteCheckSerializer(community_information)
            msg = "나눔 미완료!"
            return Response({
                    "msg": msg,
                    "community": serializer.data
                })

