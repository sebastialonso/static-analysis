# Generated by Django 2.2.16 on 2020-09-30 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patterns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ocurrencereport',
            name='commited_epoch',
            field=models.IntegerField(null=True),
        ),
    ]
