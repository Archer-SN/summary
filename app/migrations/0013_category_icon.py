# Generated by Django 4.0.4 on 2022-05-04 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_article_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
