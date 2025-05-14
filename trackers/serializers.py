from rest_framework import serializers
from trackers.models import Tracker


class TrackerSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Tracker """

    class Meta:
        model = Tracker
        fields = '__all__'

    def validate_parent(self, value):
        if value and self.instance.pk == value.pk:
            raise serializers.ValidationError(
                "Задача не может ссылаться саму на себя"
            )
            return value