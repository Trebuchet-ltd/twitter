# Generated by Django 4.2.7 on 2024-02-15 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_result_resultpage_result_pages_result_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.category'),
        ),
    ]
