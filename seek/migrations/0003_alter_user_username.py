# Generated by Django 3.2.12 on 2023-12-12 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seek', '0002_auto_20231212_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]