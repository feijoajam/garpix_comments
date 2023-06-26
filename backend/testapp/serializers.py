from rest_framework import serializers
from backend.testapp.models import MyPost


class MyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPost
        fields = '__all__'
