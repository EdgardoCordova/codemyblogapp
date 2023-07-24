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
                    img.thumpnail((300,300))
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

class Profile(models.Model):
    # la relación uno a uno será con User de Members.
    user = models.OneToOneField(User, null= True, on_delete=models.CASCADE)
    bio = models.TextField(max_length = 255)
    profile_pic = models.ImageField(null=True, blank=True, upload_to= "images/profile/")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)
    def save(self, *args, **kwargs):
        # verificar que la imagen que estoy subiendo es diferente a la predeterminada
        if self.pk and self.profile_pic != 'default.png':
            old_post = Post.objects.get(pk=self.pk)
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'default.png')

            if old_post.profile_pic.path != self.profile_pic.path and old_post.profile_pic.path != default_image_path:
                # se elimina la imagen anterior si es distinta de la actual y distinta de default.png
                default_storage.delete(old_post.profile_pic.path)

        super(Post, self).save(*args, **kwargs)

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
                    img.thumpnail((300,300))
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
