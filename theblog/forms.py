from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','title_tag','author','body')

    # ojo despues de campos no lleva "=" sino ":"    
    # el form control lo controlaremos con un <div class="form-group"> .... </div> 
    # en el html y en el widget cada item va a tener que tener un <class="form-control">
    # ojo Textarea no lleva la A en mayúscula

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo'}),
            'title_tag':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tag del título'}),
            'author':  forms.Select(attrs={'class': 'form-control'}),
            'body':  forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detalle del blog'}),
        }

class EditarForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'title_tag', 'body')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo'}),
            'title_tag':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tag del título'}),
            #'author':  forms.Select(attrs={'class': 'form-control'}),
            'body':  forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detalle del blog'}),
        }
