# Generated by Django 4.2.2 on 2023-07-15 12:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task", name="active", field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="task",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="task",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
