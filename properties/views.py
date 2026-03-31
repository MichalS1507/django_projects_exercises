from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Property, PropertyImage, Booking
from .serializers import PropertySerializer, PropertyImageSerializer, BookingSerializer, UserSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        if self.request.query_params.get('my') == 'true':
            return Property.objects.filter(owner=user)

        return Property.objects.filter(is_available=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return PropertyImage.objects.filter(property__owner=self.request.user)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []