# Generated by Django 3.2.8 on 2023-07-17 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0005_auto_20230716_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(default='coding', max_length=255),
        ),
    ]