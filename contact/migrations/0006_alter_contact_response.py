# Generated by Django 5.1 on 2024-12-15 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0005_alter_contact_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='response',
            field=models.TextField(blank=True, max_length=200, verbose_name='response'),
        ),
    ]
