import json

from flask import Flask, Response
from flask import request

from ndimensionaltictactoe.schema.requests_schema import CreateGameRequestSchema, JoinGameRequestSchema
from ndimensionaltictactoe.computation.game_service import GameService

app = Flask("ndimensionaltictactoe")
game_service = GameService()

HTTP_ERROR_CLIENT = 403
HTTP_ERROR_SERVER = 500


@app.route('/create', methods=['POST'])
def create():
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
def join():
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
