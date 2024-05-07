from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        validated_data.pop('owner')
        return super().create(validated_data)

    def validate(self, data):
        print(data)
        if ('status' in data.keys()) and (data['status'] == 'OPEN'):
            validate_status = Advertisement.objects.filter(creator=self.context["request"].user, status='OPEN')
            if validate_status.count() > 10:
                raise serializers.ValidationError('Создать можно только 10 открытых объявлений')
        return data
