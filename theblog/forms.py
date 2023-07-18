from django import forms
from .models import Post, Category

#options = [('coding','coding'),('movies','movies'),('sports','sports'),]  # hard coded, tienen que estar duplicados los valores 
options = Category.objects.all().values_list('name','name') # values_list tendra los datos duplicados

option_list = []

for item in options:
    option_list.append(item) 


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','title_tag','author', 'category','body')

    # ojo despues de campos no lleva "=" sino ":"    
    # el form control lo controlaremos con un <div class="form-group"> .... </div> 
    # en el html y en el widget cada item va a tener que tener un <class="form-control">
    # ojo Textarea no lleva la A en mayúscula

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo'}),
            'title_tag':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tag del título'}),
            'author':  forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'usuario', 'type': 'hidden'}),
            #'author':  forms.Select(attrs={'class': 'form-control'}),
            'category':  forms.Select(choices=option_list, attrs={'class': 'form-control'}),
            'body':  forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detalle del blog'}),
        }

class EditarForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'title_tag', 'category', 'body')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo'}),
            'title_tag':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tag del título'}),
            'author':  forms.Select(attrs={'class': 'form-control'}),
            'category':  forms.Select(choices=option_list, attrs={'class': 'form-control', 'placeholder': 'Categoria'}),
            'body':  forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detalle del blog'}),
        }
