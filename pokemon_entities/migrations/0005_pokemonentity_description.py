# Generated by Django 3.1.14 on 2024-10-03 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0004_auto_20241002_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonentity',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
