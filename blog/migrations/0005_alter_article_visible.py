# Generated by Django 4.2.7 on 2023-11-24 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_article_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]