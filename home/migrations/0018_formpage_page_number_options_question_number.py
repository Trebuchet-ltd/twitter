# Generated by Django 4.2.7 on 2024-02-17 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_merge_20240217_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='formpage',
            name='page_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='options',
            name='question_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
