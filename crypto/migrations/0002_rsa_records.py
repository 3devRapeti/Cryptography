# Generated by Django 5.1.1 on 2024-12-09 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crypto", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="rsa_records",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("n", models.IntegerField()),
                ("p", models.IntegerField()),
                ("q", models.IntegerField()),
                ("phi", models.IntegerField()),
                ("e", models.IntegerField()),
                ("d", models.IntegerField()),
                ("msg", models.IntegerField()),
            ],
        ),
    ]