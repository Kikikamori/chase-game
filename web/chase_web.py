"""
chase_web.py - Веб-версия игры Chase с использованием Flask
"""

from flask import Flask, render_template, jsonify, request
from chase_core import ChaseGame
import json

app = Flask(__name__)
game = None

def create_game(seed=None):
    """Создание новой игры"""
    global game
    game = ChaseGame(seed=seed)
    return game

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Создание новой игры"""
    data = request.json
    seed = data.get('seed')
    create_game(seed)
    
    return jsonify({
        'success': True,
        'board': game.get_board_string(),
        'instructions': game.get_instructions(),
        'player_pos': game.player_pos,
        'interceptors': game.interceptors
    })

@app.route('/api/move', methods=['POST'])
def make_move():
    """Выполнение хода"""
    data = request.json
    move = data.get('move')
    
    if game is None:
        create_game()
    
    result = game.process_move(move)
    
    response = {
        'success': result['valid_move'],
        'message': result['message'],
        'board': game.get_board_string(),
        'game_over': result['game_over'],
        'game_won': result.get('game_won', False),
        'game_lost': result.get('player_destroyed', False),
        'player_pos': game.player_pos,
        'interceptors': game.interceptors
    }
    
    return jsonify(response)

@app.route('/api/state', methods=['GET'])
def get_state():
    """Получение текущего состояния игры"""
    if game is None:
        create_game()
    
    return jsonify({
        'board': game.get_board_string(),
        'game_over': game.game_over,
        'player_pos': game.player_pos,
        'move_count': game.move_count
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)