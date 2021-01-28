import requests
from django import template
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from core.forms import FileForm, UploadFileForm
from core.models import Rule, File
from core.serializers import RuleSerializer


class RuleView(APIView):
    def get(self, request):
        rules = Rule.objects.all()
        serializer = RuleSerializer(rules, many=True)
        return Response({"rules": serializer.data})


class RuleCreateView(CreateView):
    model = Rule
    template_name = 'core/rule_new.html'
    fields = ['source', 'destination', 'port']


class CreateFileView(CreateView):
    model = File
    form_class = FileForm
    template_name = 'upload.html'
    success_url = reverse_lazy('home')


class RuleListView(ListView):
    model = Rule
    template_name = 'core/rule_list.html'
    pk_url_kwarg = "id"


class RuleDetailView(ListView):
    model = Rule
    template_name = 'core/rule_detail.html'
    pk_url_kwarg = "id"


class RuleUpdateView(UpdateView):
    model = Rule
    template_name = 'core/rule_edit.html'
    pk_url_kwarg = "id"
    fields = ['source', 'destination', 'port']


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
    return render(request, 'upload.html')


def index(request):
    if request.method == 'POST':
        r = requests.post('http://vrealize.iss.icl.kazan.ru', data={'number': 2525})
        print(r.status_code, r.reason)
        return HttpResponse('index.html')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            form.save()
            return HttpResponseRedirect('/rules')
    else:
        form = FileForm()
    return render(request, 'index.html', {'form': form})"""


def model_form_upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = FileForm()
    return render(request, 'index.html', {
        'form': form
    })


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class RuleList(generics.ListCreateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = RuleSerializer(queryset, many=True)
        return Response(serializer.data)
