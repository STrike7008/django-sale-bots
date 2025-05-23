import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from django.urls import reverse
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Назва")
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug'],)
        ]
        verbose_name = "Товар"
        verbose_name_plural = " Товари"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])

    def get_price(self):
        return self.discount_price if self.discount_price else self.price


@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    about = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            if self.avatar:
                img = Image.open(self.avatar.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.avatar.path)
        except Exception as e:
            print(e)

    def delete_avatar(self):
        if self.avatar:
            if os.path.isfile(self.avatar.path):
                os.remove(self.avatar.path)
            self.avatar = None
            self.save()

@receiver(pre_delete, sender=UserProfile)
def delete_avatar_on_profile_delete(sender, instance, **kwargs):
    if instance.avatar and os.path.isfile(instance.avatar.path):
        os.remove(instance.avatar.path)


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name="Товар")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    content = models.TextField(verbose_name="Коментар")
    rating = models.PositiveSmallIntegerField(verbose_name="Оцінка", choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата коментаря")

    def __str__(self):
        return f"Відгук від {self.user.username} до {self.product.name}"

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"


class BroadcastMessage(models.Model):
    message = models.TextField()
    image = models.ImageField(upload_to='broadcasts/', null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.active:
            BroadcastMessage.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.message[:20]}..." if len(self.message) > 20 else self.message

    class Meta:
        verbose_name = "Реклама"
        verbose_name_plural = "Реклама"


@receiver(post_delete, sender=BroadcastMessage)
def delete_broadcast_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
