# Generated by Django 4.2 on 2024-10-21 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_tempuser_bio_tempuser_birth_date_tempuser_gender_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="username",
        ),
    ]