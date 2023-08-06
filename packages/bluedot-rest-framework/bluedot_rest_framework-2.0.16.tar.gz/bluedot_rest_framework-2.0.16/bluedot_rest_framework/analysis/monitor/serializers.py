from rest_framework import serializers
from .models import AnalysisMonitor


class AnalysisMonitorSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        request = self.context['request']
        ip = request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get(
            'HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
        validated_data['user_ip'] = ip
        return self.Meta.model.objects.create(**validated_data)

    class Meta:
        model = AnalysisMonitor
        fields = '__all__'
