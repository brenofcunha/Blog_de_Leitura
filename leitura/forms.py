from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "summary", "content", "status"]
        labels = {
            "title": "Titulo",
            "summary": "Resumo",
            "content": "Conteudo",
            "status": "Status",
        }
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 3}),
            "content": forms.Textarea(attrs={"rows": 8}),
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
