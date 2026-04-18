from django.shortcuts import render


CATEGORIES = [
    {
        "icon": "PP",
        "title": "Programador Pragmático",
        "description": "Boas práticas para construir software sustentável e evolutivo.",
        "posts": [
            {
                "title": "Dicas práticas para codar com propósito",
                "url": "#",
            },
            {
                "title": "Automatize tarefas repetitivas",
                "url": "#",
            },
            {
                "title": "Comunicação clara entre devs",
                "url": "#",
            },
        ],
        "link": "programador_pragmatico",
    },
    {
        "icon": "CC",
        "title": "Clean Code",
        "description": "Princípios para manter o código limpo, legível e testável.",
        "posts": [
            {
                "title": "Nomes que contam histórias",
                "url": "#",
            },
            {
                "title": "Funções pequenas e coesas",
                "url": "#",
            },
            {
                "title": "Tratamento de erros sem ruído",
                "url": "#",
            },
        ],
        "link": "",
    },
    {
        "icon": "RF",
        "title": "Refactoring",
        "description": "Como melhorar design de código sem alterar comportamento.",
        "posts": [
            {
                "title": "Refatorações seguras em pequenos passos",
                "url": "#",
            },
            {
                "title": "Reduzindo duplicações críticas",
                "url": "#",
            },
            {
                "title": "Code smells no dia a dia",
                "url": "#",
            },
        ],
        "link": "",
    },
    {
        "icon": "DD",
        "title": "Domain-Driven Design",
        "description": "Modelagem de domínio para projetos complexos e de longo prazo.",
        "posts": [
            {
                "title": "Linguagem ubíqua em projetos reais",
                "url": "#",
            },
            {
                "title": "Bounded contexts sem confusão",
                "url": "#",
            },
            {
                "title": "Modelos ricos e expressivos",
                "url": "#",
            },
        ],
        "link": "",
    },
    {
        "icon": "AL",
        "title": "Entendendo Algoritmos",
        "description": "Conceitos de algoritmos com exemplos visuais e objetivos.",
        "posts": [
            {
                "title": "Busca binária explicada com casos",
                "url": "#",
            },
            {
                "title": "Big O sem complexidade desnecessária",
                "url": "#",
            },
            {
                "title": "Grafos para resolver problemas reais",
                "url": "#",
            },
        ],
        "link": "",
    },
    {
        "icon": "AR",
        "title": "Arquitetura Limpa",
        "description": "Estruturando aplicações com foco em desacoplamento e manutenção.",
        "posts": [
            {
                "title": "Camadas e fronteiras bem definidas",
                "url": "#",
            },
            {
                "title": "Regra de dependência na prática",
                "url": "#",
            },
            {
                "title": "Casos de uso testáveis",
                "url": "#",
            },
        ],
        "link": "",
    },
]

RECENT_POSTS = [
    {
        "title": "Resumo: Capítulo 1 de Programador Pragmático",
        "category": "Programador Pragmático",
        "date": "18 abr 2026",
    },
    {
        "title": "Checklist de Clean Code para revisar PRs",
        "category": "Clean Code",
        "date": "16 abr 2026",
    },
    {
        "title": "3 code smells que corrigi esta semana",
        "category": "Refactoring",
        "date": "14 abr 2026",
    },
    {
        "title": "Como organizar bounded contexts no projeto",
        "category": "DDD",
        "date": "12 abr 2026",
    },
]


def home(request):
    query = request.GET.get("q", "").strip()
    normalized_query = query.lower()

    filtered_categories = [
        category
        for category in CATEGORIES
        if not normalized_query
        or normalized_query in category["title"].lower()
        or normalized_query in category["description"].lower()
        or any(normalized_query in post["title"].lower() for post in category["posts"])
    ]

    context = {
        "query": query,
        "categories": filtered_categories,
        "recent_posts": RECENT_POSTS,
    }
    return render(request, "leitura/home.html", context)


def programador_pragmatico(request):
    return render(request, "leitura/programador_pragmatico.html")
