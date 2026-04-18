(() => {
    const STORAGE_KEY = "blog_admin_posts";

    const form = document.getElementById("postForm");
    const formCard = document.getElementById("postFormCard");
    const formTitle = document.getElementById("formTitle");
    const newPostBtn = document.getElementById("newPostBtn");
    const cancelEditBtn = document.getElementById("cancelEditBtn");
    const tableBody = document.getElementById("postsTableBody");
    const cardsContainer = document.getElementById("cardsContainer");

    const fields = {
        id: document.getElementById("postId"),
        title: document.getElementById("title"),
        summary: document.getElementById("summary"),
        content: document.getElementById("content"),
        image: document.getElementById("image"),
        date: document.getElementById("date"),
        category: document.getElementById("category"),
    };

    const categories = JSON.parse(document.getElementById("admin-categories").textContent);

    const mockedPosts = [
        {
            id: crypto.randomUUID(),
            title: "Guia de hábitos pragmáticos",
            summary: "Resumo das práticas mais úteis para manter consistência no código.",
            content: "Conteúdo detalhado do post...",
            image: "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=960&q=80",
            date: "2026-04-18",
            category: "Programador Pragmático",
        },
        {
            id: crypto.randomUUID(),
            title: "Refatorando sem medo",
            summary: "Como aplicar melhorias contínuas com segurança.",
            content: "Conteúdo detalhado do post...",
            image: "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=960&q=80",
            date: "2026-04-17",
            category: "Refactoring",
        },
    ];

    // Camada de persistencia mockada em localStorage.
    function getPosts() {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(mockedPosts));
            return [...mockedPosts];
        }

        try {
            return JSON.parse(raw);
        } catch (error) {
            console.error("Falha ao ler dados locais.", error);
            return [];
        }
    }

    function savePosts(posts) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(posts));
    }

    function resetForm() {
        form.reset();
        fields.id.value = "";
        formTitle.textContent = "Novo post";
    }

    function openForm(editing = false) {
        formCard.hidden = false;
        if (!editing) {
            resetForm();
            fields.date.value = new Date().toISOString().slice(0, 10);
        }
    }

    function closeForm() {
        formCard.hidden = true;
        resetForm();
    }

    function formatDate(dateValue) {
        if (!dateValue) {
            return "-";
        }

        const [year, month, day] = dateValue.split("-");
        return `${day}/${month}/${year}`;
    }

    function postRowTemplate(post) {
        return `
            <tr>
                <td>${post.title}</td>
                <td>${post.category}</td>
                <td>${formatDate(post.date)}</td>
                <td>
                    <div class="row-actions">
                        <button type="button" class="action-btn edit" data-action="edit" data-id="${post.id}">Editar</button>
                        <button type="button" class="action-btn delete" data-action="delete" data-id="${post.id}">Excluir</button>
                    </div>
                </td>
            </tr>
        `;
    }

    function renderTable(posts) {
        if (!posts.length) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="empty-state">Nenhum post cadastrado ainda.</td>
                </tr>
            `;
            return;
        }

        tableBody.innerHTML = posts
            .slice()
            .sort((a, b) => (a.date < b.date ? 1 : -1))
            .map(postRowTemplate)
            .join("");
    }

    function renderCategoryCards(posts) {
        const cardsHtml = categories
            .map(category => {
                const relatedPosts = posts.filter(post => post.category === category).slice(0, 3);
                const postsMarkup = relatedPosts.length
                    ? relatedPosts
                        .map(post => `<li><a href="#" title="${post.summary}">${post.title}</a></li>`)
                        .join("")
                    : `<li class="empty-state">Nenhum post nesta categoria.</li>`;

                return `
                    <article class="category-card-admin">
                        <div class="card-banner"></div>
                        <h3>${category}</h3>
                        <ul>${postsMarkup}</ul>
                    </article>
                `;
            })
            .join("");

        cardsContainer.innerHTML = cardsHtml;
    }

    function render() {
        const posts = getPosts();
        renderTable(posts);
        renderCategoryCards(posts);
    }

    function fillForm(post) {
        fields.id.value = post.id;
        fields.title.value = post.title;
        fields.summary.value = post.summary;
        fields.content.value = post.content;
        fields.image.value = post.image;
        fields.date.value = post.date;
        fields.category.value = post.category;
        formTitle.textContent = "Editar post";
        openForm(true);
    }

    // Esta funcao pode ser substituida por chamada de API (POST/PUT) no backend.
    function upsertPost(newPost) {
        const posts = getPosts();
        const idx = posts.findIndex(post => post.id === newPost.id);

        if (idx >= 0) {
            posts[idx] = newPost;
        } else {
            posts.push(newPost);
        }

        savePosts(posts);
        render();
    }

    // Esta funcao pode ser substituida por chamada DELETE no backend.
    function deletePost(postId) {
        const posts = getPosts();
        const updated = posts.filter(post => post.id !== postId);
        savePosts(updated);
        render();
    }

    newPostBtn.addEventListener("click", () => {
        openForm(false);
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    cancelEditBtn.addEventListener("click", closeForm);

    form.addEventListener("submit", event => {
        event.preventDefault();

        const postPayload = {
            id: fields.id.value || crypto.randomUUID(),
            title: fields.title.value.trim(),
            summary: fields.summary.value.trim(),
            content: fields.content.value.trim(),
            image: fields.image.value.trim(),
            date: fields.date.value,
            category: fields.category.value,
        };

        upsertPost(postPayload);
        closeForm();
    });

    tableBody.addEventListener("click", event => {
        const target = event.target;
        if (!(target instanceof HTMLElement)) {
            return;
        }

        const postId = target.dataset.id;
        const action = target.dataset.action;

        if (!postId || !action) {
            return;
        }

        const post = getPosts().find(item => item.id === postId);
        if (!post) {
            return;
        }

        if (action === "edit") {
            fillForm(post);
            window.scrollTo({ top: 0, behavior: "smooth" });
            return;
        }

        if (action === "delete") {
            const confirmed = window.confirm(`Excluir o post \"${post.title}\"?`);
            if (confirmed) {
                deletePost(postId);
            }
        }
    });

    // Inicializa dados mockados e renderiza tudo ao carregar.
    render();
})();
