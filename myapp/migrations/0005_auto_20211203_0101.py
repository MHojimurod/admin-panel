# Generated by Django 3.2.9 on 2021-12-03 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_employee_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='requests',
            name='desc',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='requests',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
