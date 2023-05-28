from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from api.models import Selection
from api.permissions import IsOwner
from api.serializers import (
    SelectionListSerializer, SelectionSerializer,
    SelectionCreateUpdateSerializer
)


class SelectionListView(generics.ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer
    permission_classes = [IsAuthenticated]


class SelectionDetailView(generics.RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]


class SelectionCreateView(generics.CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateUpdateSerializer

    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        return super().post(request)


class SelectionUpdateView(generics.UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateUpdateSerializer
    permission_classes = [IsOwner]


class SelectionDeleteView(generics.DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsOwner]