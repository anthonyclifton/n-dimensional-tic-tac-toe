import atexit
import json
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, Response
from flask import request

from ndimensionaltictactoe.schema.requests_schema import CreateGameRequestSchema, JoinGameRequestSchema, \
    LobbyRequestSchema, TournamentRequestSchema, RoundRequestSchema
from ndimensionaltictactoe.computation.game_service import GameService

app = Flask("ndimensionaltictactoe")
game_service = GameService()

HTTP_ERROR_CLIENT = 403
HTTP_ERROR_SERVER = 500

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

logging.basicConfig()


@app.route('/create', methods=['POST'])
def handle_create_game():
    create_game_json = request.get_json(silent=True)
    create_game_request, errors = CreateGameRequestSchema().load(create_game_json)

    if errors:
        print(errors)

    game_name = create_game_request.get('game_name', 'Unnamed Game')
    player_name = create_game_request.get('player_name', "Unnamed Player")
    update_url = create_game_request['update_url']

    game = game_service.create_game(game_name, player_name, update_url)

    response = Response(
        response=json.dumps(game),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/join', methods=['POST'])
def handle_join_game():
    join_game_json = request.get_json(silent=True)
    join_game_request, errors = JoinGameRequestSchema().load(join_game_json)

    game_key = join_game_request['game_key']
    player_name = join_game_request['player_name']
    update_url = join_game_request['update_url']
    game = game_service.join_game(game_key, player_name, update_url)

    response = Response(
        response=json.dumps(game),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/lobby', methods=['GET', 'POST'])
def handle_lobby():
    if request.method == 'POST':
        lobby_json = request.get_json(silent=True)
        lobby_request, errors = LobbyRequestSchema().load(lobby_json)

        player_name = lobby_request['player_name']
        update_url = lobby_request['update_url']
        player = game_service.enter_lobby(player_name, update_url)

        response = Response(
            response=json.dumps(player),
            status=200,
            mimetype='application/json'
        )
    else:
        players = game_service.get_lobby()
        response = Response(
            response=json.dumps(players),
            status=200,
            mimetype='application/json'
        )

    return response


@app.route('/tournament', methods=['GET', 'POST'])
def handle_tournament():
    if request.method == 'POST':
        tournament_json = request.get_json(silent=True)
        tournament_request, errors = TournamentRequestSchema().load(tournament_json)

        tournament_name = tournament_request['tournament_name']
        tournament = game_service.create_tournament(tournament_name)

        response = Response(
            response=json.dumps(tournament),
            status=200,
            mimetype='application/json'
        )
    else:
        tournaments = game_service.get_tournaments()
        response = Response(
            response=json.dumps(tournaments),
            status=200,
            mimetype='application/json'
        )

    return response


@app.route('/round', methods=['POST'])
def handle_round():
    round_json = request.get_json(silent=True)
    round_request, errors = RoundRequestSchema().load(round_json)

    tournament_key = round_request['tournament_key']
    x_size = round_request['x_size']
    y_size = round_request['y_size']
    winning_length = round_request['winning_length']

    round = game_service.play_round(scheduler,
                                    tournament_key,
                                    x_size,
                                    y_size,
                                    winning_length)

    response = Response(
        response=json.dumps(round),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/games', methods=['GET'])
def get_games():
    games = game_service.get_games()

    response = Response(
        response=json.dumps(games),
        status=200,
        mimetype='application/json'
    )

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3334)
