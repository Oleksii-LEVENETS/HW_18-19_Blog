# Generated by Django 4.1.7 on 2023-03-07 04:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog_users", "0003_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bloguser",
            name="first_name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="bloguser",
            name="last_name",
            field=models.CharField(max_length=50),
        ),
    ]
