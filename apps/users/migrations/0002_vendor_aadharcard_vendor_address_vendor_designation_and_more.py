# Generated by Django 4.0.4 on 2022-05-28 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='AadharCard',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='Address',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='Designation',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='Dob',
            field=models.DateField(null=True, verbose_name='Dob'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='Name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
