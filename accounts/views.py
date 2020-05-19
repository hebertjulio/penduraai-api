from rest_framework.status import HTTP_200_OK

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from rest_framework_api_key.permissions import HasAPIKey

from rest_framework_simplejwt import views as simplejwt_views

from .models import User
from .serializers import UserSerializer


class UserListView(generics.CreateAPIView):

    serializer_class = UserSerializer
    permission_classes = [HasAPIKey]


class UserDetailView(generics.RetrieveAPIView):

    lookup_field = 'pk'
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer


class LoggedUserDetailView(generics.RetrieveUpdateAPIView):

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LoggedUserDeactivateView(APIView):

    def patch(self, request, *args, **kwargs):
        obj = self.request.user
        obj.is_active = False
        obj.save()
        serializer = UserSerializer(obj)
        return Response(serializer.data, HTTP_200_OK)


class TokenObtainPairView(simplejwt_views.TokenObtainPairView):

    permission_classes = [HasAPIKey]


class TokenRefreshView(simplejwt_views.TokenRefreshView):

    permission_classes = [HasAPIKey]
