# Generated by Django 4.0.4 on 2022-05-28 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsersStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Username', models.CharField(max_length=200)),
                ('Date', models.DateField(null=True, verbose_name='ON')),
                ('In', models.TimeField(null=True, verbose_name='IN')),
                ('Mealin', models.TimeField(null=True, verbose_name='Mealin')),
                ('Mealout', models.TimeField(null=True, verbose_name='Mealout')),
                ('Out', models.TimeField(null=True, verbose_name='Out')),
                ('Vendor', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]