# Generated by Django 4.0.4 on 2022-05-10 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecomment',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.article'),
        ),
    ]