# Generated by Django 3.0.7 on 2020-07-03 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0001_initial'),
        ('credentials', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='credential',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='credentials.Credential', verbose_name='交易所凭证'),
        ),
    ]
