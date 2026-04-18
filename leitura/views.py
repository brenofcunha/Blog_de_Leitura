from django.shortcuts import render


BOOKS = [
    {
        "slug": "programador-pragmatico",
        "title": "Programador Pragmático",
        "description": "Boas práticas para construir software sustentável e evolutivo.",
        "link": "programador_pragmatico",
        "available": True,
    },
    {
        "slug": "clean-code",
        "title": "Clean Code",
        "description": "Princípios para manter o código limpo, legível e testável.",
        "link": None,
        "available": False,
    },
    {
        "slug": "refactoring",
        "title": "Refactoring",
        "description": "Como melhorar design de código sem alterar comportamento.",
        "link": None,
        "available": False,
    },
    {
        "slug": "domain-driven-design",
        "title": "Domain-Driven Design",
        "description": "Modelagem de domínio para projetos complexos e de longo prazo.",
        "link": None,
        "available": False,
    },
    {
        "slug": "algoritmos",
        "title": "Entendendo Algoritmos",
        "description": "Conceitos de algoritmos com exemplos visuais e objetivos.",
        "link": None,
        "available": False,
    },
    {
        "slug": "arquitetura-limpa",
        "title": "Arquitetura Limpa",
        "description": "Estruturando aplicações com foco em desacoplamento e manutenção.",
        "link": None,
        "available": False,
    },
]


def home(request):
    query = request.GET.get("q", "").strip()
    normalized_query = query.lower()

    filtered_books = [
        book
        for book in BOOKS
        if not normalized_query
        or normalized_query in book["title"].lower()
        or normalized_query in book["description"].lower()
    ]

    context = {
        "query": query,
        "books": filtered_books,
    }
    return render(request, "leitura/home.html", context)


def programador_pragmatico(request):
    return render(request, "leitura/programador_pragmatico.html")
