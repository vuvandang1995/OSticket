# Generated by Django 2.0.3 on 2018-04-23 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_users_status1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.CharField(max_length=255, null=True),
        ),
    ]