# Generated by Django 3.0.5 on 2020-04-29 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gymadmin', '0002_student_address'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Student',
        ),
    ]