# Generated by Django 3.2.7 on 2021-09-16 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(blank=True, to='rbac.Role'),
        ),
    ]