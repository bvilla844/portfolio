# views.py
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

def index(request):
    return render(request, 'slot/slot.html')

@api_view(['POST'])
def play_slot(request):
    data = request.data
    balance = float(data.get('balance', 0))
    bet = float(data.get('bet', 0))

    if bet <= 0 or bet > balance:
        return Response({'error': 'Invalid bet'}, status=400)

    symbols = ['🍒', '🍉', '🍋', '🍏']
    row = [random.choice(symbols) for _ in range(3)]

    payout = 0
    if row[0] == row[1] == row[2]:
        payouts = {'🍒': 5, '🍉': 10, '🍏': 20, '🍋': 50}
        payout = bet * payouts.get(row[0], 0)

    balance = balance - bet + payout

    return Response({
        'row': row,
        'payout': payout,
        'balance': round(balance, 2)
    })
