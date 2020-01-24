from typing import Dict

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import History, SearchArea, User


class SearchAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchArea
        fields = ('name', )


class HistorySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.t_user_id')

    class Meta:
        model = History
        fields = ('request', 'result', 'user')

    def create(self, validated_data: Dict) -> History:
        param_user = validated_data.get('user', {})
        t_user_id = param_user.get('t_user_id')
        try:
            user = User.objects.get(t_user_id=t_user_id)
        except ObjectDoesNotExist:
            user = User(t_user_id=t_user_id)
            user.save()
        validated_data['user'] = user
        return super().create(validated_data)
