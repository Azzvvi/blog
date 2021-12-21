from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
"""
!!! Моделька юзера создается по дефолту самим фреймворком django!!!
"""


class Post(models.Model):  # описание модели постов

    title = models.CharField(max_length=200)  # оглавление поста
    text = models.TextField()  # текст поста
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # владелец поста
    views = models.IntegerField()  # количество просмотров
    create_date = models.DateTimeField(auto_now_add=True)  # дата создания

    def get_absolute_url(self):  # получения адреса, в случае запроса для детального просмотра
        return f'news/{self.id}'

    def __str__(self):  # для удобного отображения инфо в админке\запросах на стороне сервера
        return self.title
