# Generated by Django 2.1.2 on 2018-11-03 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0019_auto_20181104_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='points',
            field=models.PositiveIntegerField(default=10, help_text='The number of points that user will get if he/she completes this                                          test case successfully. The total points later-on will be calculated as a percentage of 100', verbose_name='Points'),
        ),
    ]
