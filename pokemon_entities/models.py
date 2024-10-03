from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название покемона'
    )
    previous_evolution = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='next_evolutions',
        verbose_name='Предыдущая эволюция'
    )
    title_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Название на английском'
    )
    title_jp = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Название на японском'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    image = models.ImageField(
        blank=True,
        verbose_name='Изображение'
    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон'
    )
    lat = models.FloatField(
        verbose_name='Широта'
    )
    lon = models.FloatField(
        verbose_name='Долгота'
    )
    appeared_at = models.DateTimeField(
        verbose_name='Время появления'
    )
    disappeared_at = models.DateTimeField(
        null=True,
        verbose_name='Время исчезновения'
    )
    level = models.IntegerField(
        null=True,
        verbose_name='Уровень'
    )
    health = models.IntegerField(
        null=True,
        verbose_name='Здоровье'
    )
    strength = models.IntegerField(
        null=True,
        verbose_name='Сила'
    )
    defence = models.IntegerField(
        null=True,
        verbose_name='Защита'
    )
    stamina = models.IntegerField(
        null=True,
        verbose_name='Выносливость'
    )

    def __str__(self):
        return f'{self.pokemon} at {self.lat}, {self.lon}'
