# Generated by Django 3.2.20 on 2023-10-04 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
