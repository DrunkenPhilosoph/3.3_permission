from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from advertisements.filters import AdvertisementFilter
from advertisements.permissions import IsOwner
from advertisements.serializers import AdvertisementSerializer
from advertisements.models import Advertisement


class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    permission_classes = (IsAuthenticated, IsOwner)
    filterset_class = AdvertisementFilter
    search_fields = ('creator', 'status')

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return []

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user_id = self.request.query_params.get('creator')
        status = self.request.query_params.get('status')
        if user_id:
            queryset = Advertisement.objects.filter(creator=user_id)
        if status:
            queryset = Advertisement.objects.filter(status=status)
        return queryset