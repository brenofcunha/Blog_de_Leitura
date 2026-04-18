from django.shortcuts import render


def home(request):
    return render(request, "leitura/home.html")


def programador_pragmatico(request):
    return render(request, "leitura/programador_pragmatico.html")
