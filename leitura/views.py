from django.shortcuts import render


def home(request):
    return render(request, "leitura/home.html")


def programator_pragmatico(request):
    return render(request, "leitura/programator_pragmatico.html")
