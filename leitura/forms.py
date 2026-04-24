from django import forms

from .models import Book, Post


class PostForm(forms.ModelForm):
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
            "summary": forms.Textarea(attrs={"rows": 3}),
            "content": forms.Textarea(
                attrs={
                    "rows": 14,
                    "placeholder": "Use Markdown: # Titulo, **negrito**, listas, links e imagens",
                    "style": "font-family: Consolas, monospace;",
                }
            ),
            "categories": forms.CheckboxSelectMultiple(),
            "tags": forms.CheckboxSelectMultiple(),
        }

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


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author_name", "description", "cover_image", "status", "rating", "categories", "tags"]
        labels = {
            "title": "Titulo",
            "author_name": "Autor",
            "description": "Descricao",
            "cover_image": "Capa do livro",
            "status": "Status de leitura",
            "rating": "Avaliacao (1-5)",
            "categories": "Categorias",
            "tags": "Tags",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "categories": forms.CheckboxSelectMultiple(),
            "tags": forms.CheckboxSelectMultiple(),
        }

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        if not title:
            raise forms.ValidationError("Titulo e obrigatorio.")
        return title

    def clean_author_name(self):
        author_name = (self.cleaned_data.get("author_name") or "").strip()
        if not author_name:
            raise forms.ValidationError("Autor e obrigatorio.")
        return author_name

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is not None and not (1 <= rating <= 5):
            raise forms.ValidationError("Avaliacao deve ser entre 1 e 5.")
        return rating

    def clean_cover_image(self):
        cover_image = self.cleaned_data.get("cover_image")
        if not cover_image:
            return cover_image

        valid_extensions = (".jpg", ".jpeg", ".png", ".webp")
        name = cover_image.name.lower()
        if not name.endswith(valid_extensions):
            raise forms.ValidationError("Formato de imagem invalido. Use jpg, jpeg, png ou webp.")
        return cover_image

