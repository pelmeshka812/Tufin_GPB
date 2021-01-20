from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.generics import ListCreateAPIView

from core import views
from core.models import Rule
from core.serializers import RuleSerializer
from core.views import RuleView, CreateFileView

urlpatterns = [
    path('api/rules/', RuleView.as_view()),
    path('index/', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('upload/', CreateFileView.as_view(), name = 'upload_file'),
    path('', views.index, name = 'home'),
    path('rules/', ListCreateAPIView.as_view(queryset=Rule.objects.all(), serializer_class=RuleSerializer),
         name='rule-list')
]
