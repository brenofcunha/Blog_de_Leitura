from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.utils.text import slugify


class UserProfile(models.Model):
    ROLE_ADMIN = "admin"
    ROLE_AUTHOR = "autor"
    ROLE_CHOICES = [
        (ROLE_ADMIN, "Administrador"),
        (ROLE_AUTHOR, "Autor"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_AUTHOR)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN or self.user.is_staff or self.user.is_superuser


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    STATUS_DRAFT = "rascunho"
    STATUS_PUBLISHED = "publicado"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Rascunho"),
        (STATUS_PUBLISHED, "Publicado"),
    ]

    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=180, unique=True, db_index=True)
    summary = models.TextField(max_length=320, blank=True)
    content = models.TextField()
    cover_image = models.FileField(
        upload_to="posts/covers/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])],
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        db_index=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    categories = models.ManyToManyField(Category, related_name="posts", blank=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "published_at"], name="post_status_pub_idx"),
            models.Index(fields=["author", "status"], name="post_author_status_idx"),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:140] or "post"
            slug = base_slug
            index = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{index}"
                index += 1
            self.slug = slug

        if self.status == self.STATUS_PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()

        if self.status == self.STATUS_DRAFT:
            self.published_at = None
        super().save(*args, **kwargs)

    def can_be_managed_by(self, user):
        if not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        return self.author_id == user.id


@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, created, **kwargs):
    if created:
        active_users = User.objects.filter(is_active=True).count()
        max_users = getattr(settings, "MAX_PORTAL_USERS", 5)
        if active_users > max_users:
            instance.is_active = False
            instance.save(update_fields=["is_active"])

        default_role = (
            UserProfile.ROLE_ADMIN
            if (instance.is_staff or instance.is_superuser)
            else UserProfile.ROLE_AUTHOR
        )
        UserProfile.objects.create(user=instance, role=default_role)
    else:
        profile, _ = UserProfile.objects.get_or_create(user=instance)
        expected_role = (
            UserProfile.ROLE_ADMIN
            if (instance.is_staff or instance.is_superuser)
            else profile.role
        )
        if profile.role != expected_role and (instance.is_staff or instance.is_superuser):
            profile.role = expected_role
            profile.save(update_fields=["role"])
