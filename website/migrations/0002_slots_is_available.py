# Generated by Django 3.2.4 on 2021-12-14 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slots',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]