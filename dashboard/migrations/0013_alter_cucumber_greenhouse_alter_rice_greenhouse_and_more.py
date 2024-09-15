# Generated by Django 4.2.13 on 2024-09-15 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0012_greenhouse_total_square_units"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cucumber",
            name="greenhouse",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cucumber",
                to="dashboard.greenhouse",
            ),
        ),
        migrations.AlterField(
            model_name="rice",
            name="greenhouse",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rice",
                to="dashboard.greenhouse",
            ),
        ),
        migrations.AlterField(
            model_name="tomato",
            name="greenhouse",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tomato",
                to="dashboard.greenhouse",
            ),
        ),
    ]