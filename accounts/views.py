from rest_framework.status import HTTP_200_OK

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from rest_framework_api_key.permissions import HasAPIKey

from rest_framework_simplejwt import views as simplejwt_views

from .models import User, Profile, Whitelist
from .serializers import UserSerializer, ProfileSerializer, WhitelistSerializer


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
        user = self.request.user
        return user


class LoggedUserDeactivateView(APIView):

    def patch(self, request, *args, **kwargs):
        obj = self.request.user
        obj.is_active = False
        obj.save()
        serializer = UserSerializer(obj)
        res = Response(serializer.data, HTTP_200_OK)
        return res


class TokenObtainPairView(simplejwt_views.TokenObtainPairView):

    permission_classes = [HasAPIKey]


class TokenRefreshView(simplejwt_views.TokenRefreshView):

    permission_classes = [HasAPIKey]


class ProfileListView(generics.ListCreateAPIView):

    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Profile.objects.filter(accountable=user)
        return qs


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Profile.objects.filter(accountable=user)
        return qs


class WhitelistListView(generics.ListCreateAPIView):

    serializer_class = WhitelistSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Whitelist.objects.filter(user=user)
        return qs


class WhitelistDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = WhitelistSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Whitelist.objects.filter(user=user)
        return qs


class CreditorListView(generics.ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        qs = User.objects.filter(
            id__in=user.debtor.values_list('creditor').distinct())
        return qs


class DebtorListView(generics.ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        qs = User.objects.filter(
            id__in=user.creditor.values_list('debtor').distinct())
        return qs
