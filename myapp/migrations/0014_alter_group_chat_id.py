# Generated by Django 3.2.9 on 2021-12-11 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_alter_requesttypes_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='chat_id',
            field=models.CharField(max_length=255),
        ),
    ]
