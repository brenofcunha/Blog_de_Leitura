from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone

from leitura.models import Category, Post, Tag


class LeituraPagesTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.autor = self.user_model.objects.create_user(username="autor1", password="123456789")
        self.outro_autor = self.user_model.objects.create_user(username="autor2", password="123456789")

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portal de leitura")

    def test_posts_list_only_published(self):
        Post.objects.create(
            title="Publico",
            summary="Resumo publico",
            content="Conteudo publico",
            status=Post.STATUS_PUBLISHED,
            author=self.autor,
            published_at=timezone.now(),
        )
        Post.objects.create(
            title="Rascunho",
            summary="Resumo rascunho",
            content="Conteudo rascunho",
            status=Post.STATUS_DRAFT,
            author=self.autor,
        )

        response = self.client.get(reverse("post_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Publico")
        self.assertNotContains(response, "Rascunho")

    def test_post_detail_by_slug(self):
        post = Post.objects.create(
            title="Detalhe publico",
            summary="Resumo detalhe",
            content="Conteudo detalhe",
            status=Post.STATUS_PUBLISHED,
            author=self.autor,
            published_at=timezone.now(),
        )

        response = self.client.get(reverse("post_detail", kwargs={"slug": post.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detalhe publico")
        self.assertContains(response, "Conteudo detalhe")

    def test_post_detail_returns_404_for_missing_slug(self):
        response = self.client.get(reverse("post_detail", kwargs={"slug": "slug-inexistente"}))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_blocks_draft_from_public(self):
        draft = Post.objects.create(
            title="Rascunho secreto",
            summary="Resumo secreto",
            content="Conteudo secreto",
            status=Post.STATUS_DRAFT,
            author=self.autor,
        )

        response = self.client.get(reverse("post_detail", kwargs={"slug": draft.slug}))
        self.assertEqual(response.status_code, 404)

    def test_admin_area_requires_login(self):
        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_create_post_as_draft(self):
        self.client.login(username="autor1", password="123456789")
        response = self.client.post(
            reverse("admin_post_new"),
            {
                "title": "Novo post",
                "summary": "Resumo novo",
                "content": "Conteudo novo",
                "status": Post.STATUS_DRAFT,
                "action": "save_draft",
            },
        )
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(title="Novo post")
        self.assertEqual(post.status, Post.STATUS_DRAFT)
        self.assertEqual(post.author, self.autor)
        self.assertEqual(post.slug, slugify("Novo post"))

    def test_publish_post(self):
        self.client.login(username="autor1", password="123456789")
        response = self.client.post(
            reverse("admin_post_new"),
            {
                "title": "Post publico",
                "summary": "Resumo",
                "content": "Conteudo",
                "status": Post.STATUS_DRAFT,
                "action": "publish",
            },
        )
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(title="Post publico")
        self.assertEqual(post.status, Post.STATUS_PUBLISHED)
        self.assertIsNotNone(post.published_at)

    def test_edit_post_antigo(self):
        post = Post.objects.create(
            title="Titulo antigo",
            summary="Resumo antigo",
            content="Conteudo antigo",
            status=Post.STATUS_DRAFT,
            author=self.autor,
        )
        self.client.login(username="autor1", password="123456789")
        response = self.client.post(
            reverse("admin_post_edit", kwargs={"post_id": post.id}),
            {
                "title": "Titulo atualizado",
                "summary": "Resumo atualizado",
                "content": "Conteudo atualizado",
                "status": Post.STATUS_DRAFT,
                "action": "save",
            },
        )
        self.assertEqual(response.status_code, 302)
        post.refresh_from_db()
        self.assertEqual(post.title, "Titulo atualizado")
        self.assertEqual(post.content, "Conteudo atualizado")

    def test_list_posts_with_filter_by_status(self):
        Post.objects.create(
            title="Post publicado unico",
            summary="Resumo",
            content="Conteudo",
            status=Post.STATUS_PUBLISHED,
            author=self.autor,
        )
        Post.objects.create(
            title="Rascunho interno",
            summary="Resumo",
            content="Conteudo",
            status=Post.STATUS_DRAFT,
            author=self.autor,
        )

        self.client.login(username="autor1", password="123456789")
        response = self.client.get(reverse("admin_posts"), {"status": Post.STATUS_DRAFT})

        self.assertContains(response, "Rascunho interno")
        self.assertNotContains(response, "Post publicado unico")

    def test_prevent_edit_without_permission(self):
        post = Post.objects.create(
            title="Privado",
            summary="Resumo",
            content="Conteudo",
            status=Post.STATUS_DRAFT,
            author=self.autor,
        )

        self.client.login(username="autor2", password="123456789")
        response = self.client.post(
            reverse("admin_post_edit", kwargs={"post_id": post.id}),
            {
                "title": "Tentativa",
                "summary": "Tentativa",
                "content": "Tentativa",
                "status": Post.STATUS_DRAFT,
                "action": "save",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_public_search_filters_posts(self):
        Post.objects.create(
            title="Django avançado",
            summary="Resumo",
            content="Conteudo sobre ORM",
            status=Post.STATUS_PUBLISHED,
            author=self.autor,
            published_at=timezone.now(),
        )
        Post.objects.create(
            title="Post de Java",
            summary="Resumo",
            content="Conteudo Java",
            status=Post.STATUS_PUBLISHED,
            author=self.autor,
            published_at=timezone.now(),
        )

        response = self.client.get(reverse("post_list"), {"q": "django"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django avançado")
        self.assertNotContains(response, "Post de Java")

    def test_filter_by_category_and_tag(self):
        categoria_backend = Category.objects.create(name="Backend")
        categoria_front = Category.objects.create(name="Frontend")
        tag_python = Tag.objects.create(name="Python")
        tag_css = Tag.objects.create(name="CSS")

        post_backend = Post.objects.create(
            title="API com Django",
            summary="Resumo",
            content="Conteudo",
            status=Post.STATUS_PUBLISHED,
            author=self.autor,
            published_at=timezone.now(),
        )
        post_backend.categories.add(categoria_backend)
        post_backend.tags.add(tag_python)

        post_front = Post.objects.create(
            title="Layout com CSS",
            summary="Resumo",
            content="Conteudo",
            status=Post.STATUS_PUBLISHED,
            author=self.autor,
            published_at=timezone.now(),
        )
        post_front.categories.add(categoria_front)
        post_front.tags.add(tag_css)

        response_categoria = self.client.get(reverse("post_list"), {"categoria": categoria_backend.slug})
        self.assertContains(response_categoria, "API com Django")
        self.assertNotContains(response_categoria, "Layout com CSS")

        response_tag = self.client.get(reverse("post_list"), {"tag": tag_css.slug})
        self.assertContains(response_tag, "Layout com CSS")
        self.assertNotContains(response_tag, "API com Django")

    def test_public_list_has_pagination(self):
        for index in range(8):
            Post.objects.create(
                title=f"Post {index}",
                summary="Resumo",
                content="Conteudo",
                status=Post.STATUS_PUBLISHED,
                author=self.autor,
                published_at=timezone.now(),
            )

        response_page_1 = self.client.get(reverse("post_list"))
        response_page_2 = self.client.get(reverse("post_list"), {"page": 2})

        self.assertEqual(response_page_1.status_code, 200)
        self.assertContains(response_page_1, "Pagina 1 de 2")
        self.assertContains(response_page_2, "Pagina 2 de 2")


class ModelTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.author = self.user_model.objects.create_user(username="model_autor", password="123456789")

    def test_user_creation(self):
        user = self.user_model.objects.create_user(username="novo_usuario", password="senha_segura")
        self.assertTrue(user.pk is not None)
        self.assertEqual(user.username, "novo_usuario")

    def test_post_creation(self):
        post = Post.objects.create(
            title="Post de modelo",
            summary="Resumo",
            content="Conteudo",
            status=Post.STATUS_DRAFT,
            author=self.author,
        )
        self.assertTrue(post.pk is not None)
        self.assertEqual(post.status, Post.STATUS_DRAFT)

    def test_slug_uniqueness(self):
        first = Post.objects.create(
            title="Mesmo titulo",
            summary="Resumo 1",
            content="Conteudo 1",
            status=Post.STATUS_DRAFT,
            author=self.author,
        )
        second = Post.objects.create(
            title="Mesmo titulo",
            summary="Resumo 2",
            content="Conteudo 2",
            status=Post.STATUS_DRAFT,
            author=self.author,
        )
        self.assertNotEqual(first.slug, second.slug)

    def test_publication_status_sets_published_at(self):
        post = Post.objects.create(
            title="Publicacao",
            summary="Resumo",
            content="Conteudo",
            status=Post.STATUS_PUBLISHED,
            author=self.author,
        )
        self.assertEqual(post.status, Post.STATUS_PUBLISHED)
        self.assertIsNotNone(post.published_at)


class PermissionTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.author_a = self.user_model.objects.create_user(username="autor_a", password="123456789")
        self.author_b = self.user_model.objects.create_user(username="autor_b", password="123456789")
        self.admin = self.user_model.objects.create_user(
            username="admin_user",
            password="123456789",
            is_staff=True,
        )
        self.post = Post.objects.create(
            title="Post do autor A",
            summary="Resumo",
            content="Conteudo",
            status=Post.STATUS_DRAFT,
            author=self.author_a,
        )

    def test_author_cannot_edit_another_author_post(self):
        self.client.login(username="autor_b", password="123456789")
        response = self.client.post(
            reverse("admin_post_edit", kwargs={"post_id": self.post.id}),
            {
                "title": "Edicao indevida",
                "summary": "Resumo",
                "content": "Conteudo",
                "status": Post.STATUS_DRAFT,
                "action": "save",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_admin_can_edit_any_post(self):
        self.client.login(username="admin_user", password="123456789")
        response = self.client.post(
            reverse("admin_post_edit", kwargs={"post_id": self.post.id}),
            {
                "title": "Edicao admin",
                "summary": "Resumo alterado",
                "content": "Conteudo alterado",
                "status": Post.STATUS_DRAFT,
                "action": "save",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Edicao admin")

    def test_unauthenticated_user_blocked_from_admin_edit(self):
        response = self.client.get(reverse("admin_post_edit", kwargs={"post_id": self.post.id}))
        self.assertEqual(response.status_code, 302)


class BookCRUDTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user_a = self.user_model.objects.create_user(username="leitor_a", password="123456789")
        self.user_b = self.user_model.objects.create_user(username="leitor_b", password="123456789")
        self.admin = self.user_model.objects.create_user(
            username="admin_livros",
            password="123456789",
            is_staff=True,
        )

    def _make_book(self, user=None, title="Livro teste", author_name="Autor teste"):
        from leitura.models import Book
        return Book.objects.create(
            title=title,
            author_name=author_name,
            status=Book.STATUS_WISHLIST,
            added_by=user or self.user_a,
        )

    def test_book_list_requires_login(self):
        response = self.client.get(reverse("admin_books"))
        self.assertEqual(response.status_code, 302)

    def test_book_list_shows_own_books(self):
        self._make_book(user=self.user_a, title="Meu livro A")
        self._make_book(user=self.user_b, title="Livro do B")
        self.client.login(username="leitor_a", password="123456789")
        response = self.client.get(reverse("admin_books"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Meu livro A")
        self.assertNotContains(response, "Livro do B")

    def test_admin_sees_all_books(self):
        self._make_book(user=self.user_a, title="Livro do usuario A")
        self._make_book(user=self.user_b, title="Livro do usuario B")
        self.client.login(username="admin_livros", password="123456789")
        response = self.client.get(reverse("admin_books"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Livro do usuario A")
        self.assertContains(response, "Livro do usuario B")

    def test_create_book(self):
        self.client.login(username="leitor_a", password="123456789")
        response = self.client.post(
            reverse("admin_book_new"),
            {
                "title": "Dom Quixote",
                "author_name": "Cervantes",
                "description": "Classico espanhol.",
                "status": "quero_ler",
            },
        )
        self.assertEqual(response.status_code, 302)
        from leitura.models import Book
        book = Book.objects.get(title="Dom Quixote")
        self.assertEqual(book.added_by, self.user_a)
        self.assertEqual(book.status, Book.STATUS_WISHLIST)

    def test_edit_own_book(self):
        book = self._make_book(user=self.user_a, title="Titulo original")
        self.client.login(username="leitor_a", password="123456789")
        response = self.client.post(
            reverse("admin_book_edit", kwargs={"book_id": book.id}),
            {
                "title": "Titulo editado",
                "author_name": "Autor teste",
                "description": "",
                "status": "lido",
            },
        )
        self.assertEqual(response.status_code, 302)
        book.refresh_from_db()
        self.assertEqual(book.title, "Titulo editado")
        self.assertEqual(book.status, "lido")

    def test_cannot_edit_another_users_book(self):
        book = self._make_book(user=self.user_a, title="Privado")
        self.client.login(username="leitor_b", password="123456789")
        response = self.client.post(
            reverse("admin_book_edit", kwargs={"book_id": book.id}),
            {
                "title": "Tentativa",
                "author_name": "Autor teste",
                "description": "",
                "status": "lendo",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_own_book(self):
        from leitura.models import Book
        book = self._make_book(user=self.user_a)
        self.client.login(username="leitor_a", password="123456789")
        response = self.client.post(reverse("admin_book_delete", kwargs={"book_id": book.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(pk=book.id).exists())

    def test_cannot_delete_another_users_book(self):
        book = self._make_book(user=self.user_a)
        self.client.login(username="leitor_b", password="123456789")
        response = self.client.post(reverse("admin_book_delete", kwargs={"book_id": book.id}))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_delete_any_book(self):
        from leitura.models import Book
        book = self._make_book(user=self.user_a)
        self.client.login(username="admin_livros", password="123456789")
        response = self.client.post(reverse("admin_book_delete", kwargs={"book_id": book.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(pk=book.id).exists())

    def test_book_slug_uniqueness(self):
        from leitura.models import Book
        first = Book.objects.create(
            title="Mesmo titulo",
            author_name="Mesmo autor",
            status=Book.STATUS_WISHLIST,
            added_by=self.user_a,
        )
        second = Book.objects.create(
            title="Mesmo titulo",
            author_name="Mesmo autor",
            status=Book.STATUS_WISHLIST,
            added_by=self.user_a,
        )
        self.assertNotEqual(first.slug, second.slug)


class LoginRedirectTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username="redirect_user", password="123456789")

    def test_login_redirect_requires_auth(self):
        response = self.client.get(reverse("post_login_redirect"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response["Location"])

    def test_login_redirect_goes_to_dashboard(self):
        self.client.login(username="redirect_user", password="123456789")
        response = self.client.get(reverse("post_login_redirect"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("admin", response["Location"])
