import requests

from ndimensionaltictactoe.computation.game_renderer import render_game_outcome
from ndimensionaltictactoe.models.game import GAME_INPROGRESS, GAME_COMPLETED
from ndimensionaltictactoe.models.mark import X_MARK, O_MARK
from ndimensionaltictactoe.schema.game_schema import MoveSchema, GameSchema


def _generic_post(url, game):
    dumped_game, errors = GameSchema().dump(game)

    response = requests.post(url, json=dumped_game)
    move, errors = MoveSchema().loads(response.content)
    return move


def _shutdown_post(url):
    requests.post(url, json={})


def game_thread(game, pvp_mode=False):
    move_counter = game.size_x * game.size_y
    while game.state == GAME_INPROGRESS and move_counter > 0:
        if game.player_x_turn:
            move = _generic_post("{}/update".format(game.player_x.update_url), game)
            winner = game.mark_cell_by_coordinates(move['x'], move['y'], X_MARK)
            if winner:
                game.player_x.winner = True
                game.player_o.winner = False
            move_counter = move_counter - 1
            game.player_x_turn = False
        else:
            move = _generic_post("{}/update".format(game.player_o.update_url), game)
            winner = game.mark_cell_by_coordinates(move['x'], move['y'], O_MARK)
            if winner:
                game.player_x.winner = False
                game.player_o.winner = True
            move_counter = move_counter - 1
            game.player_x_turn = True

    if game.state == GAME_INPROGRESS:
        game.player_x.winner = False
        game.player_o.winner = False
        game.state = GAME_COMPLETED

    _game_completed(game, pvp_mode)
    return game


def _game_completed(game, pvp_mode):
    _generic_post("{}/update".format(game.player_x.update_url), game)
    _generic_post("{}/update".format(game.player_o.update_url), game)

    if pvp_mode:
        render_game_outcome(game)
        _shutdown_post("{}/shutdown".format(game.player_x.update_url))
        _shutdown_post("{}/shutdown".format(game.player_o.update_url))


