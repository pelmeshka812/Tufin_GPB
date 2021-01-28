from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.generics import ListCreateAPIView

from core import views
from core.models import Rule
from core.serializers import RuleSerializer
from core.views import RuleView, CreateFileView, RuleListView, RuleDetailView, RuleUpdateView, RuleCreateView

urlpatterns = [
    path('api/rules/', RuleView.as_view()),
    path('index/', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('upload/', views.model_form_upload, name='upload_file'),
    # path('home/', TemplateView.as_view(template_name='core/rule_bad.html'), name='home'),
    # path('rules/', ListCreateAPIView.as_view(queryset=Rule.objects.all(), serializer_class=RuleSerializer),
    # name='rule-list'),
    path('', RuleListView.as_view(), name='list'),
    path('rule/<int:id>/', RuleDetailView.as_view(), name='rule_detail'),
    path('rule/<int:id>/edit/', RuleUpdateView.as_view(), name='rule_edit'),
    path('rules/new/', RuleCreateView.as_view(), name='rule_new')
]
