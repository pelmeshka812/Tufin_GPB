import requests
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from core.forms import FileForm
from core.models import Rule, File
from core.serializers import RuleSerializer


class RuleView(APIView):
    def get(self, request):
        rules = Rule.objects.all()
        serializer = RuleSerializer(rules, many=True)
        return Response({"rules": serializer.data})


class CreateFileView(CreateView):
    model = File
    form_class = FileForm
    template_name = 'upload.html'
    success_url = reverse_lazy('home')


"""def excel_file(request):
    if request.method == 'POST':
        form = ExcelForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('home/')
    else:
        form = ExcelForm()
    return render(request, 'index.html', {'form': form})


def upload(request):
    if request.method == 'POST' and request.FILES['excel']:
        excel = request.FILES['excel']
        fs = FileSystemStorage()
        filename = fs.save(excel.name, excel)
        return render(request, 'index.html')


def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        return render(request, 'upload.html')
    return render(request, 'upload.html')"""


def index(request):
    if request.method == 'POST':
        r = requests.post('http://vrealize.iss.icl.kazan.ru', data={'number': 2525})
        print(r.status_code, r.reason)
        return HttpResponse('index.html')


class RuleList(generics.ListCreateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = RuleSerializer(queryset, many=True)
        return Response(serializer.data)
