# Generated by Django 3.2.8 on 2023-07-26 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0015_alter_profile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(max_length=600),
        ),
    ]
