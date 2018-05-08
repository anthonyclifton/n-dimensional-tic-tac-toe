import json
from time import sleep
from uuid import uuid4

import requests

from ndimensionaltictactoe.common import notify_error, log_api_call
from flask import Flask, Response
from flask import jsonify
from flask import request

from ndimensionaltictactoe.ndimensionaltictactoe import ndimensionaltictactoe_call, ndimensionaltictactoe_list
from ndimensionaltictactoe.schema.requests_schema import CreateGameRequestSchema
from ndimensionaltictactoe.computation.game_service import GameService

app = Flask("ndimensionaltictactoe")
game_service = GameService()

HTTP_ERROR_CLIENT = 403
HTTP_ERROR_SERVER = 500


@app.route('/ndimensionaltictactoe/call', methods=['GET'])
def ndimensionaltictactoe_call_api():
    if 'host' not in request.args or request.args['host'] in ("", None):
        return notify_error("ERR_NO_ARG: 'host' argument required /ndimensionaltictactoe/test", HTTP_ERROR_CLIENT)

    try:
        host = str(request.args.get('host'))
    except:
        return notify_error("ERR_INVALID_TYPE:  'host' parameter must be a string", HTTP_ERROR_CLIENT)

    try:
        return jsonify(answer=ndimensionaltictactoe_call(host))
    except Exception as ex:
        return notify_error(ex, HTTP_ERROR_SERVER)


@app.route('/ndimensionaltictactoe/list', methods=['GET'])
@log_api_call
def ndimensionaltictactoe_list_api():
    if 'apikey' not in request.args or request.args['apikey'] in ("", None):
        return notify_error("ERR_NO_ARG: 'apikey' argument required /ndimensionaltictactoe/list", HTTP_ERROR_CLIENT)

    try:
        apikey = str(request.args.get('apikey'))
    except:
        return notify_error("ERR_INVALID_TYPE:  'apikey' parameter must be a string", HTTP_ERROR_CLIENT)

    try:
        return jsonify(answer=ndimensionaltictactoe_list(apikey))
    except Exception as ex:
        return notify_error(ex, HTTP_ERROR_SERVER)


@app.route('/create', methods=['POST'])
def create():
    create_game_json = request.get_json(silent=True)
    create_game_request, errors = CreateGameRequestSchema().load(create_game_json)
    game = game_service.create_game(create_game_request['game_name'])

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
