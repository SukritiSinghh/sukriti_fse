# Generated by Django 5.1.6 on 2025-02-24 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_alter_financialdocument_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financialdocument',
            name='status',
        ),
    ]
