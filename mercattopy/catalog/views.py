from django.http import request, HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
   return render (request, "catalog/base.html")

# def home(request):
#     html = """
#     <h1>Senac Site Online</h1>
#     <p>Meu primeiro back-end com Django está funcionando.</p>
#     """
#     return HttpResponse(html)