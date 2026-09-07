from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.replace('ı', 'i'))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts", verbose_name="Yazar")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="posts", verbose_name="Kategori")
    summary = models.TextField(max_length=500, verbose_name="Kısa Özet")
    content = models.TextField(verbose_name="İçerik")
    image = models.ImageField(upload_to="blog/", blank=True, null=True, verbose_name="Kapak Görseli")
    is_published = models.BooleanField(default=True, verbose_name="Yayınlandı mı?")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Görüntülenme Sayısı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Yazısı"
        verbose_name_plural = "Blog Yazıları"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title.replace('ı', 'i'))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title