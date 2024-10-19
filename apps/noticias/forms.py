from django import forms
from .models import Noticia, Categoria, Denuncia

class NoticiaForm(forms.ModelForm):
    categoria_noticia = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        empty_label="Selecciona una categoría",
        required=True
    )

    class Meta:
        model = Noticia
        fields = ['titulo', 'cuerpo', 'imagen', 'categoria_noticia']


class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['motivo']