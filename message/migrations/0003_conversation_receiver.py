# Generated by Django 3.2.20 on 2023-09-09 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0002_conversation_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='receiver',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
