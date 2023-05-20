# Generated by Django 4.1.7 on 2023-02-18 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.TextField(max_length=300)),
                ('description', models.TextField(max_length=1000)),
                ('done', models.BooleanField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField()),
            ],
        ),
    ]
