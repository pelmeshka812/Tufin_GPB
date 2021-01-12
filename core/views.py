from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Rule
from core.serializers import RuleSerializer


class RuleView(APIView):
    def get(self, request):
        rules = Rule.objects.all()
        serializer = RuleSerializer(rules, many=True)
        return Response({"rules" : serializer.data})
