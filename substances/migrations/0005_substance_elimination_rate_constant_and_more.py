# Generated by Django 4.0.6 on 2022-12-13 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substances', '0004_alter_dosageformdose_dosage_alter_doserecord_roi_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='substance',
            name='elimination_rate_constant',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='substance',
            name='half_life',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='substance',
            name='volume_of_distribution',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]