from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Ads
from api.permissions import IsOwner, IsAdmin
from api.serializers import AdsSerializer, AdCreateSerializer, AdUpdateSerializer


@permission_classes([IsAuthenticated])
class AdsListView(generics.ListAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer

    def get(self, request, *args, **kwargs):
        # Filter by category by id
        category = request.GET.get('cat', None)
        if category:
            self.queryset = self.queryset.filter(
                category__id=category
            )

        # Filter by text in ad name
        text = request.GET.get('text', None)
        if text:
            self.queryset = self.queryset.filter(
                name__icontains=text
            )

        # Filter by location
        location = request.GET.get('location', None)
        if location:
            self.queryset = self.queryset.filter(
                author__location__name__icontains=location
            )

        # Filter by price
        price_from = request.GET.get('price_from', None)
        price_to = request.GET.get('price_to', None)
        match (
            price_from.isdigit() if price_from else None,
            price_to.isdigit() if price_to else None
        ):
            case (True, None):
                self.queryset = self.queryset.filter(price__gte=price_from)
            case (None, True):
                self.queryset = self.queryset.filter(price__lte=price_to)
            case (True, True):
                if int(price_from) > int(price_to):
                    return Response(
                        {'error': 'Price from greater than price to!'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                self.queryset = self.queryset.filter(price__range=(price_from, price_to))
            case _:
                pass

        return super().get(request, *args, **kwargs)


@permission_classes([IsAuthenticated])
class AdDetailView(generics.RetrieveAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer


class AdCreateView(generics.CreateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdCreateSerializer

    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        return super().post(request)


class AdUpdateView(generics.UpdateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsOwner | IsAdmin]


class AdDeleteView(generics.DestroyAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [IsOwner | IsAdmin]