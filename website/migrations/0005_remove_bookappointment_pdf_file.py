# Generated by Django 4.0 on 2022-01-18 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_bookappointment_conformation_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookappointment',
            name='pdf_file',
        ),
    ]