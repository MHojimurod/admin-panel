# Generated by Django 3.2.9 on 2021-12-03 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_employee_confirmer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='confirmer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.employee'),
        ),
    ]
