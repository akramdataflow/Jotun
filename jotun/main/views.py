from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def main_view(request):
    return HttpResponse('<h1>hi<h1/>')