# Generated by Django 4.2.3 on 2023-07-14 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
                ('authors', models.CharField(max_length=255)),
                ('categories', models.CharField(max_length=255)),
                ('publication_date', models.DateField()),
                ('editor', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.URLField(blank=True)),
            ],
        ),
    ]
