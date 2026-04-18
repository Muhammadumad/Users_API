import uuid

from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100, trim_whitespace=True)
    email = serializers.EmailField()
    age = serializers.IntegerField(min_value=0)

    def create(self, validated_data):
        return {
            'id': uuid.uuid4(),
            'name': validated_data['name'],
            'email': validated_data['email'],
            'age': validated_data['age'],
        }

    def update(self, instance, validated_data):
        instance['name'] = validated_data.get('name', instance['name'])
        instance['email'] = validated_data.get('email', instance['email'])
        instance['age'] = validated_data.get('age', instance['age'])
        return instance