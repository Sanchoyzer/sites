# Generated by Django 3.0.2 on 2020-01-24 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Область поиска')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_user_id', models.PositiveIntegerField(db_index=True, verbose_name='id пользователя в Телеграм')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.CharField(max_length=128, verbose_name='Запрос')),
                ('result', models.TextField(max_length=128, verbose_name='Результат')),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date published')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geobot.User', verbose_name='Пользователь в Телеграм')),
            ],
        ),
    ]
