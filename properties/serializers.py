from rest_framework import serializers
from .models import Property, PropertyImage, Booking
from django.contrib.auth.models import User

class PropertyImageSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'image_url', 'is_main', 'property']
        read_only_fields = ['id']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

    def validate(self, data):
        property_obj = data.get('property')
        is_main = data.get('is_main', False)

        if property_obj and is_main:
            existing_main = PropertyImage.objects.filter(property=property_obj,
                is_main=True).exclude(pk=self.instance.pk if self.instance
                else None)

            if existing_main.exists():
                raise serializers.ValidationError("This property already has a"
                                                  " main image. Only one main "
                                                  "image is allowed.")
        return data

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Property
        fields = ['id', 'title', 'description', 'price', 'address', 'city',
                  'zip_code', 'property_type', 'offer_type', 'bedrooms',
                  'bathrooms', 'area', 'is_available', 'created_at', 'updated_at',
                  'images', 'owner']
        read_only_fields = ['id', 'created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())
    property_detail = PropertySerializer(source='property', read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Booking
        fields = ['id', 'property', 'property_detail', 'message', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'property_detail']

    def validate(self, data):
        property_obj = data.get('property')
        user = self.context['request'].user

        if property_obj and property_obj.owner == user:
            raise serializers.ValidationError("You cannot book your own property.")
        return data

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user