from api.permissions import IsAdminUserOrReadOnly
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class ModelMixinSet(CreateModelMixin, DestroyModelMixin, ListModelMixin,
                    GenericViewSet):
    permission_classes = (IsAdminUserOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'
