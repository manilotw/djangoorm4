import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime
from pokemon_entities.models import Pokemon,PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    current_time = localtime()
    pokemons = PokemonEntity.objects.filter(appeared_at__lt=current_time,disappeared_at__gt=current_time)
    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon_entities.image.url)
            )
    pokemons = Pokemon.objects.all()
    
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })


    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    current_time = localtime()

    pokemon = get_object_or_404(Pokemon,id=pokemon_id) 

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=current_time,disappeared_at__gt=current_time,pokemon_entities=pokemon)
    entities = []
    for pokemon_entity in pokemon_entities:
        entities.append({
            'level': pokemon_entity.level,
            'lat': pokemon_entity.lat,
            'lon': pokemon_entity.lon,
            'health': pokemon_entity.health,
            'strength': pokemon_entity.strength,
            'defence': pokemon_entity.defence,
            'stamina': pokemon_entity.stamina,
        })

        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon_entities.image.url)
            )
    pokemon_data = {
        'pokemon_id' : pokemon_id,
        'title_ru' : pokemon.title,
        'title_en' : pokemon.title_en,
        'title_jp' : pokemon.title_jp,
        'description':pokemon.description,
        'img_url' : request.build_absolute_uri(pokemon.image.url),
        'entities' : entities,
        }
    
    if pokemon.previous_evolution:
        pokemon_data['previous_evolution'] = {
            'pokemon_id': pokemon.previous_evolution.id,
            'title_ru': pokemon.previous_evolution.title,
            'img_url': request.build_absolute_uri(pokemon.previous_evolution.image.url),
        }    

    next_evolutions = pokemon.next_evolutions.all()  
    if next_evolutions.exists():
        pokemon_data['next_evolution'] = []
        for next_evolution in next_evolutions:
            pokemon_data['next_evolution'] = {
                'pokemon_id': next_evolution.id,
                'title_ru': next_evolution.title,
                'img_url': request.build_absolute_uri(next_evolution.image.url),
            }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })
