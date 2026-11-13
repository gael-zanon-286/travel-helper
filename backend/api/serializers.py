from rest_framework import serializers

from api.models import TestModel


class ModelSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=100)
    message = serializers.CharField(style={"base_template": "textarea.html"})

    def create(self, validated_data):
        """
        Create and return a new `TestModel` instance, given the validated data.
        """
        return TestModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `TestModel` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.message = validated_data.get("message", instance.message)
        instance.save()
        return instance