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
