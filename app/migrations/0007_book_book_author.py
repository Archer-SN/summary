# Generated by Django 4.0.4 on 2022-05-01 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_article_thumbnail_articlecomment_thumbnail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_author',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
