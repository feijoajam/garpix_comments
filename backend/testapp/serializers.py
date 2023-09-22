from rest_framework import serializers
from testapp.models import MyPost


class MyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPost
        fields = '__all__'
