# Generated by Django 4.2.3 on 2023-10-01 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0002_alter_repayment_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]