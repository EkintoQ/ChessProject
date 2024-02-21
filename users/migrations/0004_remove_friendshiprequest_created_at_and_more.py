# Generated by Django 5.0 on 2024-02-10 07:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_country_customuser_friends_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendshiprequest',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='friendshiprequest',
            name='is_accepted',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='friends',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='total_games',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='friendshiprequest',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendshiprequest',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL),
        ),
    ]