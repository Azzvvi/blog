# Generated by Django 3.1.13 on 2021-12-14 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_post_owner'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]