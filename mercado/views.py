from django.shortcuts import render

def mercado(request):
    return render(request, "Mercado.html", {})
