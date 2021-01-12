from django.contrib import admin
from django.urls import path

from core.views import RuleView

urlpatterns = [
    path('rules/', RuleView.as_view()),
]
