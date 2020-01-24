from django.db import models


class User(models.Model):
    t_user_id = models.PositiveIntegerField(verbose_name='id пользователя в Телеграм', db_index=True)

    def __str__(self):
        return str(self.t_user_id)


class SearchArea(models.Model):
    name = models.CharField(verbose_name='Область поиска', max_length=128)

    def __str__(self):
        return self.name


class History(models.Model):
    request = models.CharField(verbose_name='Запрос', max_length=128)
    result = models.TextField(verbose_name='Результат', max_length=128)
    user = models.ForeignKey('User', verbose_name='Пользователь в Телеграм', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='date published', auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.date}, {self.user}'
