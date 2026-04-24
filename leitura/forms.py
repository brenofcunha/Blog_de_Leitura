from django import forms

from .models import Category, Post, Tag


class PostForm(forms.ModelForm):
    CLASSIFICATION_CHOICES = [
        ("", "Selecione"),
        ("Artigo", "Artigo"),
        ("Guia", "Guia"),
        ("Resenha", "Resenha"),
        ("Opiniao", "Opiniao"),
    ]
    QUICK_CATEGORY_OPTIONS = ["Literatura", "Tecnologia", "Produtividade", "Educacao"]
    QUICK_TAG_OPTIONS = ["Leitura", "Dicas", "Iniciante", "Avancado"]

    classification = forms.ChoiceField(
        required=False,
        choices=CLASSIFICATION_CHOICES,
        label="Classificacao",
        widget=forms.Select(attrs={"class": "admin-input"}),
    )
    custom_classification = forms.CharField(
        required=False,
        label="Classificacao personalizada",
        widget=forms.TextInput(
            attrs={
                "class": "admin-input",
                "placeholder": "Ex.: Tutorial, Checklist, Entrevista",
            }
        ),
    )
    custom_categories = forms.CharField(
        required=False,
        label="Categorias personalizadas",
        widget=forms.TextInput(
            attrs={
                "class": "admin-input",
                "placeholder": "Ex.: Design, Negocios, Carreira",
            }
        ),
        help_text="Separe por virgula.",
    )
    custom_tags = forms.CharField(
        required=False,
        label="Tags personalizadas",
        widget=forms.TextInput(
            attrs={
                "class": "admin-input",
                "placeholder": "Ex.: ux, narrativa, escrita",
            }
        ),
        help_text="Separe por virgula.",
    )

    class Meta:
        model = Post
        fields = ["title", "summary", "content", "cover_image", "categories", "tags", "status"]
        labels = {
            "title": "Titulo",
            "summary": "Resumo",
            "content": "Conteudo",
            "cover_image": "Imagem de capa",
            "categories": "Categorias",
            "tags": "Tags",
            "status": "Status",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "admin-input",
                    "placeholder": "Ex.: Como criar um habito de leitura consistente",
                }
            ),
            "summary": forms.Textarea(
                attrs={
                    "class": "admin-input admin-textarea",
                    "rows": 4,
                    "placeholder": "Resumo curto que aparecera em listas e destaque.",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "admin-input admin-textarea admin-content-editor",
                    "rows": 16,
                    "placeholder": "Use Markdown: # Titulo, **negrito**, listas, links e imagens",
                }
            ),
            "cover_image": forms.ClearableFileInput(attrs={"class": "admin-file-input"}),
            "status": forms.RadioSelect(attrs={"class": "status-option-input"}),
            "categories": forms.CheckboxSelectMultiple(attrs={"class": "admin-choice-input"}),
            "tags": forms.CheckboxSelectMultiple(attrs={"class": "admin-choice-input"}),
        }
        help_texts = {"cover_image": "Formatos aceitos: JPG, PNG ou WEBP."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categories"].queryset = self.fields["categories"].queryset.order_by("name")
        self.fields["tags"].queryset = self.fields["tags"].queryset.order_by("name")

        if self.instance and self.instance.pk:
            first_tag = self.instance.tags.order_by("name").first()
            if first_tag:
                self.fields["classification"].initial = first_tag.name

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        if not title:
            raise forms.ValidationError("Titulo e obrigatorio.")
        return title

    def clean_content(self):
        content = (self.cleaned_data.get("content") or "").strip()
        if not content:
            raise forms.ValidationError("Conteudo e obrigatorio.")
        return content

    def clean_cover_image(self):
        cover_image = self.cleaned_data.get("cover_image")
        if not cover_image:
            return cover_image

        valid_extensions = (".jpg", ".jpeg", ".png", ".webp")
        name = cover_image.name.lower()
        if not name.endswith(valid_extensions):
            raise forms.ValidationError("Formato de imagem invalido. Use jpg, jpeg, png ou webp.")
        return cover_image

    def save_related(self, post):
        categories = list(self.cleaned_data.get("categories") or [])
        tags = list(self.cleaned_data.get("tags") or [])

        categories.extend(self._get_or_create_categories(self.cleaned_data.get("custom_categories", "")))
        tags.extend(self._get_or_create_tags(self.cleaned_data.get("custom_tags", "")))

        classification = (
            (self.cleaned_data.get("custom_classification") or "").strip()
            or (self.cleaned_data.get("classification") or "").strip()
        )
        if classification:
            tags.extend(self._get_or_create_tags(classification))

        unique_categories = {item.pk: item for item in categories if item and item.pk}
        unique_tags = {item.pk: item for item in tags if item and item.pk}

        post.categories.set(unique_categories.values())
        post.tags.set(unique_tags.values())

    def _parse_custom_values(self, raw_value):
        seen = set()
        values = []
        for value in (raw_value or "").split(","):
            cleaned = value.strip()
            key = cleaned.lower()
            if cleaned and key not in seen:
                values.append(cleaned)
                seen.add(key)
        return values

    def _get_or_create_categories(self, raw_value):
        result = []
        for name in self._parse_custom_values(raw_value):
            category, _ = Category.objects.get_or_create(name=name)
            result.append(category)
        return result

    def _get_or_create_tags(self, raw_value):
        result = []
        for name in self._parse_custom_values(raw_value):
            tag, _ = Tag.objects.get_or_create(name=name)
            result.append(tag)
        return result
