# Generated by Django 4.0 on 2022-01-25 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_delete_doctor_alter_blog_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
    ]
