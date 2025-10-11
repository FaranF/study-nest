from django.shortcuts import get_object_or_404
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.mixins import (
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    CreateModelMixin,
)

from .models import *
from .serializers import *
from .pagination import DefaultPagination
from .filters import ProfileFilter


class ProfileViewSet(
    RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet
):
    queryset = Profile.objects.select_related("user").all()
    permission_classes = [IsAdminUser]

    pagination_class = DefaultPagination
    search_fields = ["user__first_name", "user__last_name"]
    ordering_fields = ["user__first_name", "user__last_name", "role"]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProfileFilter

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return ProfileUpdateSerializer
        return ProfileSerializer

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        profile = get_object_or_404(Profile, user=user)

        if request.method == "GET":
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)

        elif request.method == "PUT":
            serializer = ProfileUpdateSerializer(
                profile, data=request.data, partial=True, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class RegisterViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = RegisterProfileSerializer
    queryset = Profile.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.validated_data.pop("user")
        profile_data = serializer.validated_data

        with transaction.atomic():
            user = User.objects.create_user(**user_data)
            profile = Profile.objects.create(user=user, **profile_data)

        return Response(
            RegisterProfileSerializer(profile).data, status=status.HTTP_201_CREATED
        )
