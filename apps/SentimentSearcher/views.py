from django.shortcuts import render, HttpResponse
from .models import Search

# Create your views here.
def home(request):
    return render(request, "home.html")


def search(request):
    posts = Search.objects.all()
    return render(request, "search.html", {"search": posts})