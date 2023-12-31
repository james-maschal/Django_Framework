# Generated by Django 4.2 on 2023-04-26 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jns', '0003_alter_interfacecounters_report_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('int_name', models.CharField(max_length=200)),
                ('date', models.DateField(verbose_name='date')),
                ('switch', models.CharField(max_length=200)),
                ('temperature', models.DecimalField(decimal_places=0, max_digits=7)),
            ],
        ),
    ]
