# Generated by Django 2.1.2 on 2018-11-16 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import registration.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('email_confirmed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GoogleAuth',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('google_id', models.CharField(blank=True, max_length=250, null=True, unique=True)),
                ('salt', models.CharField(blank=True, max_length=250, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name Of Institute')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', models.CharField(blank=True, max_length=11, validators=[registration.models.phone_number_validator], verbose_name='Phone Number')),
                ('designation', models.CharField(choices=[('STU', 'Student'), ('PROF', 'Professor'), ('TA', 'Teaching Assistant')], default='STU', max_length=5, verbose_name='Designation Of User')),
                ('institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='registration.Institute')),
            ],
        ),
    ]
