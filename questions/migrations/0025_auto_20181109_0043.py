# Generated by Django 2.1.2 on 2018-11-08 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0024_auto_20181109_0041'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testcase',
            options={'ordering': ['question', 'number']},
        ),
    ]
