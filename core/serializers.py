from rest_framework import serializers


class RuleSerializer(serializers.Serializer):
    source = serializers.CharField(max_length=500)
    destination = serializers.CharField(max_length=500)
    port = serializers.CharField(max_length=500)
    status = serializers.CharField(max_length=50)
