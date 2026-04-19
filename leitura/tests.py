from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from leitura.models import Post


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
