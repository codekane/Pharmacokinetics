# Generated by Django 4.0.6 on 2022-11-27 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substances', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dosageform',
            name='name',
            field=models.CharField(default='Dexedrine XR Spansule', max_length=30),
            preserve_default=False,
        ),
    ]
