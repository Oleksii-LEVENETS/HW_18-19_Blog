# Generated by Django 4.1.7 on 2023-03-06 15:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog_app", "0005_post_draft"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="draft",
            field=models.BooleanField(default=False),
        ),
    ]