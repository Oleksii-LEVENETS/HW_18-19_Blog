# Generated by Django 4.1.7 on 2023-03-06 16:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog_app", "0006_alter_post_draft"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="draft",
            field=models.BooleanField(),
        ),
    ]
