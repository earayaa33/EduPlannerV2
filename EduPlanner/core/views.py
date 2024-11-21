from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def inicio (request):
    return render(request,'core/inicio.html')

def segunda (request):
    return render(request,'core/pagina2.html')    