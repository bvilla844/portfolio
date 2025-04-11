from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .game_logic import initialize_game, process_move
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Renderiza la terminal interactiva del juego

def index(request):
    # Recuperamos los nombres de los jugadores desde la sesión o asignamos valores predeterminados
    jugador1 = request.session.get('jugador1', 'Jugador 1')
    jugador2 = request.session.get('jugador2', 'Jugador 2')

    # Pasamos los valores al contexto para que se puedan usar en la plantilla
    context = {
        'jugador1': jugador1,
        'jugador2': jugador2,
    }

    return render(request, 'battleship/battleship.html', context)

# Inicializa un nuevo juego
@api_view(['POST'])
def start_game(request):
    jugador1 = request.data.get('jugador1')
    jugador2 = request.data.get('jugador2')
    
    # Guardar los nombres de los jugadores en la sesión
    request.session['jugador1'] = jugador1
    request.session['jugador2'] = jugador2
    
    # Inicializar el juego (puedes agregar la lógica aquí)
    game_state = initialize_game()
    
    return Response(game_state)

@api_view(['GET'])
def get_player_names(request):
    jugador1 = request.session.get('jugador1')
    jugador2 = request.session.get('jugador2')
    return Response({
        'jugador1': jugador1,
        'jugador2': jugador2
    })


# Procesa un disparo del jugador
@api_view(['POST'])
def make_move(request):
    jugador = request.data.get('jugador')
    objetivo = request.data.get('objetivo')
    x = int(request.data.get('x'))
    y = int(request.data.get('y'))

    barcos_objetivo = request.session.get(f'barcos_{objetivo}', [])

    hit = any(barco['x'] == x and barco['y'] == y for barco in barcos_objetivo)

    # Si acertó, marcamos esa coordenada como destruida
    if hit:
        barcos_objetivo = [b for b in barcos_objetivo if not (b['x'] == x and b['y'] == y)]
        request.session[f'barcos_{objetivo}'] = barcos_objetivo

    juego_terminado = len(barcos_objetivo) == 0

    return Response({
        'resultado': 'hit' if hit else 'miss',
        'coordenada': {'x': x, 'y': y},
        'juego_terminado': juego_terminado,
        'ganador': jugador if juego_terminado else None
    })



@api_view(['POST'])
def place_ships(request):
    data = request.data
    print("Datos recibidos:", data)

    jugador = data.get('jugador')
    barcos = data.get('barcos', [])

    # Guarda los barcos en la sesión usando el nombre del jugador
    request.session[f'barcos_{jugador}'] = barcos
    request.session.modified = True  # Asegura que Django guarde la sesión

    return JsonResponse({'mensaje': 'Barcos colocados exitosamente'})

