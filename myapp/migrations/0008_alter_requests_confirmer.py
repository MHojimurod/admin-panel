# Generated by Django 3.2.9 on 2021-12-04 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_employee_confirmer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='confirmer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Tasdiqlovchi', to='myapp.employee'),
        ),
    ]
