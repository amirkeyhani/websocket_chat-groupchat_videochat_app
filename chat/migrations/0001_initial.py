# Generated by Django 4.0.6 on 2022-07-22 12:45

import chat.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('unique_code', models.CharField(default=chat.models.UniqueGenerator, max_length=10)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2022, 7, 22, 17, 15, 17, 564869))),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VideoThread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('started_at', models.DateTimeField(default=datetime.datetime(2022, 7, 22, 17, 15, 17, 566946))),
                ('ended_at', models.DateTimeField(default=datetime.datetime(2022, 7, 22, 17, 15, 17, 566946))),
                ('created_at', models.DateTimeField(default=datetime.datetime(2022, 7, 22, 17, 15, 17, 566946))),
                ('callee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='callee_user', to=settings.AUTH_USER_MODEL)),
                ('caller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caller_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2022, 7, 22, 17, 15, 17, 566946))),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.groupchat')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2022, 7, 22, 17, 15, 17, 565939))),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.groupchat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
