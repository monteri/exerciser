# Generated by Django 4.2.2 on 2023-10-21 12:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pdp", "0002_alter_circle_user_useraccount"),
    ]

    operations = [
        migrations.AddField(
            model_name="circle",
            name="depth",
            field=models.PositiveIntegerField(default=0),
        ),
    ]