from rest_framework import generics, views
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response

from rest_framework_simplejwt import views as simplejwt_views
from rest_framework_api_key.permissions import HasAPIKey

from bridges.decorators import load_transaction

from .permissions import IsOwner, IsManager
from .serializers import UserSerializer, SignUpSerializer, ProfileSerializer


class SignUpView(views.APIView):

    permission_classes = [
        HasAPIKey
    ]

    def post(self, request, version):  # skipcq
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        serializer = UserSerializer(obj)
        response = Response(serializer.data, status=HTTP_201_CREATED)
        return response


class CurrentUserDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = UserSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsOwner()]
        return permissions

    def get_object(self):
        user = self.request.user
        return user

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class TokenObtainPairView(simplejwt_views.TokenObtainPairView):

    permission_classes = [
        HasAPIKey
    ]


class TokenRefreshView(simplejwt_views.TokenRefreshView):

    permission_classes = [
        HasAPIKey
    ]


class ProfileListView(generics.ListAPIView):

    serializer_class = ProfileSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsManager()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        qs = user.userprofiles.filter(is_active=True)
        return qs


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'pk'
    serializer_class = ProfileSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions += [IsManager()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        qs = user.userprofiles.filter(is_active=True)
        return qs


class ProfileCreateView(views.APIView):

    permission_classes = [
        HasAPIKey
    ]

    @load_transaction(scope='profile', status='awaiting')
    def post(self, request, version, token, transaction=None):  # skipcq
        request.data.update(transaction.payload)
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        transaction.status = 'accepted'
        transaction.save()
        response = Response(serializer.data, status=HTTP_201_CREATED)
        return response
