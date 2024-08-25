from django.db.models import Q
from rest_framework import permissions, viewsets, mixins, response, status
from rest_framework.decorators import action

from . import models
from . import serializers


class ObjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ObjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Object.objects.my_objects(self.request.user)


class BorrowViewSet(
    mixins.CreateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.BorrowSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def lent(self, request):
        lent = models.Borrow.objects.filter(object__owner__user=self.request.user)        
        serializer = self.get_serializer(lent, many=True)
        return response.Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def borrowed(self, request):
        borrowed = models.Borrow.objects.filter(borrower__user=self.request.user)
        serializer = self.get_serializer(borrowed, many=True)
        return response.Response(serializer.data)
    
    @action(detail=True, methods=["put"])
    def return_borrowed_object(self, request, pk=None):
        borrowed = self.get_object()
        if borrowed.borrower.user.id != self.request.user.id:
            return response.Response({"borrower": "Logged in user is not a borrower"}, status=status.HTTP_400_BAD_REQUEST)
        borrowed.borrower = None
        borrowed.status = "Returned"
        borrowed.save()
        serializer = self.get_serializer(borrowed)
        return response.Response(serializer.data)


    def get_queryset(self):
        lent = models.Borrow.objects.filter(object__owner__user=self.request.user)
        borrowed = models.Borrow.objects.filter(borrower__user=self.request.user)
        return lent | borrowed