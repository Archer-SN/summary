# Generated by Django 4.0.4 on 2022-05-01 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_book_book_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='name',
            new_name='title',
        ),
    ]
