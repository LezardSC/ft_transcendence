# Generated by Django 4.2.9 on 2024-03-04 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='title',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
