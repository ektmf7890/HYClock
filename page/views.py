from django.shortcuts import render

# Create your views here.

def privacy(request):
    return render(request, "page/privacy.html", {})