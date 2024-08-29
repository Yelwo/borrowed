from rest_framework import permissions, viewsets, mixins, response, status
from rest_framework.decorators import action

from . import models
from . import serializers


class ObjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ObjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Object.objects.filter(owner__user=self.request.user)


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
    
    @action(detail=False, methods=["post"])
    def borrow(self, request):
        borrow = self.get_serializer(data=request.data)
        borrow.is_valid()
        if borrow.validated_data['borrower'].user.id == self.request.user.id:
            return response.Response({"borrower": "You can't borrow your own items"}, status=status.HTTP_400_BAD_REQUEST)
        if borrow.validated_data['object'].owner.user.id != self.request.user.id:
            return response.Response({"object": "Logged in user is not an owner"}, status=status.HTTP_400_BAD_REQUEST)
        if models.Borrow.objects.filter(object=borrow.validated_data['object'], status='Borrowed'):
            return response.Response({"object": "Object has been already borrowed"}, status=status.HTTP_400_BAD_REQUEST)
        borrow.save()
        return response.Response(borrow.data)

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