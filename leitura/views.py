from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


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
    category = {
        "title": "Programador Pragmático",
        "subtitle": "Lições práticas para escrever software sustentável",
        "description": (
            "Uma trilha de leitura com foco em decisões reais de engenharia,"
            " colaboração em equipe e melhoria contínua do código."
        ),
        "reading_progress": 42,
    }

    posts = [
        {
            "slug": "mentalidade-pragmatica",
            "title": "Mentalidade pragmática no dia a dia",
            "date": "18 abr 2026",
            "summary": "Como transformar princípios do livro em hábitos simples de execução.",
            "is_featured": True,
            "read_time": "8 min",
        },
        {
            "slug": "tracer-bullets",
            "title": "Tracer bullets para validar ideias rápido",
            "date": "16 abr 2026",
            "summary": "Valide hipóteses com pequenos incrementos antes de escalar a solução.",
            "is_featured": False,
            "read_time": "6 min",
        },
        {
            "slug": "ortogonalidade",
            "title": "Ortogonalidade e baixo acoplamento",
            "date": "14 abr 2026",
            "summary": "Estruture módulos independentes para evoluir o projeto com segurança.",
            "is_featured": False,
            "read_time": "7 min",
        },
        {
            "slug": "automacao",
            "title": "Automação de tarefas repetitivas",
            "date": "12 abr 2026",
            "summary": "Scripts e checklists que economizam tempo e reduzem erros humanos.",
            "is_featured": False,
            "read_time": "5 min",
        },
    ]

    featured_post = next((post for post in posts if post["is_featured"]), posts[0])
    post_list = [post for post in posts if post["slug"] != featured_post["slug"]]

    chapters = [
        "Capítulo 1 - Uma filosofia pragmática",
        "Capítulo 2 - Um jeito pragmático",
        "Capítulo 3 - A caixa de ferramentas",
        "Capítulo 4 - Pragmatismo paranoico",
    ]

    context = {
        "category": category,
        "featured_post": featured_post,
        "posts": post_list,
        "chapters": chapters,
        # Estrutura pronta para trocar por consulta ao banco futuramente.
        # Exemplo: category = Category.objects.prefetch_related("posts").get(slug=...)
    }
    return render(request, "leitura/programador_pragmatico.html", context)


@login_required
def pos_login_redirect(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect("painel_admin")
    return redirect("home")


@login_required
def painel_admin(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect("home")

    context = {
        "categories": [category["title"] for category in CATEGORIES],
    }
    return render(request, "leitura/painel_admin.html", context)
