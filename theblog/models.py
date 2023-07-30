from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField
import os
from django.conf import settings
# se tiene que importar el Image de PILLOW
from PIL import Image

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True, blank=True, upload_to= "images/")
    title_tag = models.CharField(max_length=255)
    snippet = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #body = models.TextField()
    body = RichTextField(blank=True, null=True)
    post_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255)
    likes = models.ManyToManyField(User, related_name='blog_posts')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.header_image:
            try:
                # Abrir la imagen
                img = Image.open(self.header_image.path)

                # Redimensionar proporcionalmente la imagen si es demasiado grande (por ejemplo, a un máximo de 1000 píxeles de ancho)
                max_width = 300
                if img.width > max_width:
                    # Calcular la altura proporcional
                    proportion = max_width / img.width
                    height = int(img.height * proportion)

                    # Redimensionar la imagen
                    img = img.resize((max_width, height), Image.ANTIALIAS)
                    img.save(self.header_image.path)

            except Exception as e:
                print(f"Error al procesar la imagen: {str(e)}")
   
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        #return reverse('article-detail', args=(str(self.id)))
        return reverse('home')

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #return reverse('article-detail', args=(str(self.id)))
        return reverse('home')

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

class Profile(models.Model):
    # la relación uno a uno será con User de Members.
    user = models.OneToOneField(User, null= True, on_delete=models.CASCADE)
    bio = models.TextField(max_length = 2000)
    profile_pic = models.ImageField(null=True, blank=True, upload_to= "images/profile/")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_pic:
            try:
                # Abrir la imagen
                print("Redimensionando imagen ...")
                img = Image.open(self.profile_pic.path)
                ancho, altura = img.size
                # Redimensionar la imagen si es demasiado grande (por ejemplo, a 1000x1000 píxeles)
                max_size = (300, 300)
                print(ancho, altura)

                if img.width > max_size[0] or img.height > max_size[1]:
                    img.thumbnail(max_size, Image.ANTIALIAS)
                    img.save(self.profile_pic.path)

                # Recortar la imagen si es necesario (por ejemplo, recortar a un cuadrado de 200x200 píxeles desde el centro)
                crop_size = 200

                if img.width > crop_size and img.height > crop_size:
                    left = (img.width - crop_size) / 2
                    top = (img.height - crop_size) / 2
                    right = (img.width + crop_size) / 2
                    bottom = (img.height + crop_size) / 2
                    img = img.crop((left, top, right, bottom))
                    img.save(self.profile_pic.path)

            except Exception as e:
                # Manejar excepciones al trabajar con imágenes
                print(f"Error al procesar la imagen: {str(e)}")

    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        #return reverse('article-detail', args=(str(self.id)))
        return reverse('home')    

""" def save(self, *args, **kwargs):

        # verificar que la imagen que estoy subiendo es diferente a la predeterminada
        
        if self.pk and self.header_image != 'default.png':
            old_post = Post.objects.get(pk=self.pk)
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'default.png')

            if old_post.header_image.path != self.header_image.path and old_post.header_image.path != default_image_path:
                # se elimina la imagen anterior si es distinta de la actual y distinta de default.png
                default_storage.delete(old_post.header_image.path)

        super(Post, self).save(*args, **kwargs)

        # codigo para recortar y redimensionar la imagen
        if self.header_image and os.path.exists(self.header_image.path):
            # redimensionar la imagen
            with Image.open(self.header_image.path) as img:
                ancho, alto = img.size  # en pixels
                if ancho > alto:
                    # imagen horizontal
                    nuevo_alto = 300
                    nuevo_ancho = int((ancho/alto)*nuevo_alto)
                    img = img.resize((nuevo_ancho, nuevo_alto))
                    img.save(self.header_image.path)
                elif alto > ancho:
                    # imagen vertical
                    nuevo_ancho = 300
                    nuevo_alto = int((alto/ancho)*nuevo_ancho)
                    img = img.resize((nuevo_ancho, nuevo_alto))
                    img.save(self.header_image.path)
                else:
                    # imagen cuadrada
                    img.thumbnail((300,300))
            # recortar la imagen
            with Image.open(self.header_image.path) as img:
                ancho, alto = img.size  # en pixels
                if ancho > alto:
                    # imagen horizontal
                    left = (ancho - alto) / 2
                    top = 0
                    right = (ancho + alto) / 2
                    bottom = alto
                else:
                    left = 0
                    top = (alto - ancho ) / 2
                    right = ancho
                    bottom = (alto + ancho) / 2
                img = img.crop((left, top, right,bottom))
                img.save(self.header_image.path)
    """       



""" def save(self, *args, **kwargs):
        # verificar que la imagen que estoy subiendo es diferente a la predeterminada
        if self.pk and self.profile_pic != 'default.png':
            old_post = Post.objects.get(pk=self.pk)
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'default.png')

            if old_post.profile_pic.path != self.profile_pic.path and old_post.profile_pic.path != default_image_path:
                # se elimina la imagen anterior si es distinta de la actual y distinta de default.png
                default_storage.delete(old_post.profile_pic.path)

        super(Profile, self).save(*args, **kwargs)

        # codigo para recortar y redimensionar la imagen
        if self.profile_pic and os.path.exists(self.profile_pic.path):
            # redimensionar la imagen
            with Image.open(self.profile_pic.path) as img:
                ancho, alto = img.size  # en pixels
                if ancho > alto:
                    # imagen horizontal
                    nuevo_alto = 300
                    nuevo_ancho = int((ancho/alto)*nuevo_alto)
                    img = img.resize((nuevo_ancho, nuevo_alto))
                    img.save(self.profile_pic.path)
                elif alto > ancho:
                    # imagen vertical
                    nuevo_ancho = 300
                    nuevo_alto = int((alto/ancho)*nuevo_ancho)
                    img = img.resize((nuevo_ancho, nuevo_alto))
                    img.save(self.profile_pic.path)
                else:
                    # imagen cuadrada
                    img.thumbnail((300,300))
            # recortar la imagen
            with Image.open(self.profile_pic.path) as img:
                ancho, alto = img.size  # en pixels
                if ancho > alto:
                    # imagen horizontal
                    left = (ancho - alto) / 2
                    top = 0
                    right = (ancho + alto) / 2
                    bottom = alto
                else:
                    left = 0
                    top = (alto - ancho ) / 2
                    right = ancho
                    bottom = (alto + ancho) / 2
                img = img.crop((left, top, right,bottom))
                img.save(self.profile_pic.path)
"""
