from rest_framework import permissions, viewsets

from . import models
from . import serializers


class ObjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ObjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Object.objects.filter(owner__user=self.request.user)


class BorrowViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BorrowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        lent = models.Borrow.objects.filter(object__owner__user=self.request.user)
        borrowed = models.Borrow.objects.filter(borrower__user=self.request.user)
        return lent.union(borrowed)
        