from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):

    def get_absolute_url(self):
        return reverse('page_user', kwargs={'user_id': self.pk})

    class Meta:
        db_table = 'CustomUser_app_db'


class Game_account(models.Model):
    name_of_game = models.ForeignKey('Name_of_game', on_delete=models.PROTECT, verbose_name='Название игры')
    description = models.CharField(max_length=255, verbose_name='Описание')
    date_of_sale = models.DateTimeField(auto_now_add=True)
    date_of_last_purchase = models.DateTimeField(auto_now=True)
    price = models.IntegerField(default=0, verbose_name='Цена')
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name='Продавец')
    is_published = models.BooleanField(default=True, verbose_name='Продажа')

    class Meta:
        db_table = 'Game_account_app_db'

class Name_of_game(models.Model):
    game_name = models.CharField(max_length=255)
    photo_game = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')
    quantity_purchased = models.IntegerField(default=0)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    class Meta:
        db_table = 'Name_of_game_app_db'

    def __str__(self):
        return self.game_name

    def get_absolute_url(self):
        return reverse('game', kwargs={'game_name': self.game_name})

class Category(models.Model):
    category_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'Category_app_db'

    def __str__(self):
        return self.category_name