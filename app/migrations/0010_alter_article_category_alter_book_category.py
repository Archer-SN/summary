# Generated by Django 4.0.4 on 2022-05-02 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_article_category_article_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(to='app.category'),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(to='app.category'),
        ),
    ]
