# Generated by Django 4.0 on 2022-01-18 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_remove_doctormodel_gog_link'),
        ('website', '0006_alter_bookappointment_conformation_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Doctor',
        ),
        migrations.AlterField(
            model_name='blog',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to='staff.doctormodel'),
        ),
    ]