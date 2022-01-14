# Generated by Django 4.0 on 2022-01-14 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_slots_is_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, upload_to='media/image'),
        ),
        migrations.AlterField(
            model_name='bookappointment',
            name='phone',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='slots',
            name='available_slots',
            field=models.IntegerField(default=5),
        ),
    ]