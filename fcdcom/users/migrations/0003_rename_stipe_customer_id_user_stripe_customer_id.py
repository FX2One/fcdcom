# Generated by Django 4.2.7 on 2023-11-27 14:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_stipe_customer_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="stipe_customer_id",
            new_name="stripe_customer_id",
        ),
    ]
