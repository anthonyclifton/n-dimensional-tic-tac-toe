import unittest
from random import randint
from uuid import UUID

import pytest
from mock import MagicMock

from ndimensionaltictactoe.computation.game_service import GameService
from ndimensionaltictactoe.exceptions.game_inprogress_exception import GameInprogressException
from ndimensionaltictactoe.models.game import Game, GAME_INPROGRESS, GAME_COMPLETED


class TestGameService(unittest.TestCase):
    def setUp(self):
        self.game_name = 'Test Game'
        self.player_x_name = 'Test Player X'
        self.update_url = 'http://domain/update'
        self.game_service = GameService()

        self.game = self.game_service.create_game(self.game_name,
                                                  self.player_x_name,
                                                  self.update_url)

        self.game_key = UUID(self.game['key'])
        self.player_x_key = UUID(self.game['player_x']['key'])

    def test__create_game__should_return_a_dictionary(self):
        self.assertEqual(self.game['name'], self.game_name)
        self.assertEqual(self.game['size_x'], 3)
        self.assertEqual(self.game['size_y'], 3)
        self.assertEqual(self.game['player_x']['name'], self.player_x_name)
        self.assertEqual(self.game['cells'], [])
        self.assertEqual(self.game['winning_length'], 3)

    def test__create_game__should_add_a_default_game_object(self):
        game = self.game_service.get_game_by_key(UUID(self.game['key']))

        assert isinstance(game, Game)
        assert game.key == self.game_key
        assert game.size_x == 3
        assert game.size_y == 3
        assert game.dimensions == 2
        assert game.player_x_turn

    def test__create_game_should_add_an_arbitrary_sized_game(self):
        random_game_size_x = randint(0, 999)
        random_game_size_y = randint(0, 999)
        custom_sized_game = self.game_service.create_game(
            self.game_name,
            self.player_x_name,
            self.update_url,
            grid_size_x=random_game_size_x,
            grid_size_y=random_game_size_y)
        game = self.game_service.get_game_by_key(UUID(custom_sized_game['key']))
        assert game.size_x == random_game_size_x
        assert game.size_y == random_game_size_y

    def test__join_game__should_add_player_o_to_game(self):
        joined_game = self.game_service.join_game(self.game_key,
                                                  'Test Player O',
                                                  self.update_url)

        updated_game = self.game_service.get_game_by_key(self.game_key)

        assert updated_game.player_o
        assert UUID(str(updated_game.player_o.key))
        assert updated_game.player_o.name == 'Test Player O'
        assert updated_game.state == GAME_INPROGRESS

        self.assertEqual(joined_game['name'], self.game_name)
        assert UUID(joined_game['key'])
        self.assertEqual(joined_game['size_x'], 3)
        self.assertEqual(joined_game['size_y'], 3)
        assert UUID(joined_game['player_o']['key'])
        self.assertEqual(joined_game['player_o']['name'], updated_game.player_o.name)
        self.assertEqual(joined_game['cells'], [])
        self.assertEqual(joined_game['winning_length'], 3)

    def test__join_game__should_raise_exception_when_game_already_in_progress(self):
        self.game_service.join_game(self.game_key,
                                    'player who is on time',
                                    self.update_url)

        with pytest.raises(GameInprogressException):
            self.game_service.join_game(self.game_key,
                                        'player who is too late',
                                        self.update_url)

    def test__delete_game__should_remove_game_from_service(self):
        assert self.game_service.get_game_by_key(self.game_key)

        self.game_service.delete_game(self.game_key)

        with pytest.raises(KeyError):
            self.game_service.get_game_by_key(self.game_key)

    def test__get_games__should_return_all_created_games_summary(self):
        self.game_service.create_game('Test Game 2',
                                      self.player_x_name,
                                      self.update_url)

        games_list = self.game_service.get_games()

        self.assertEqual(len(games_list), 2)

    def test__enter_lobby__should_add_the_player_to_the_lobby_map(self):
        player = self.game_service.enter_lobby(self.player_x_name, self.update_url)

        self.assertEqual(self.game_service.lobby[UUID(player['key'])].name, self.player_x_name)

    def test__get_lobby__should_return_all_players_in_the_lobby(self):
        self.game_service.enter_lobby(self.player_x_name, self.update_url)
        self.game_service.enter_lobby('another player', self.update_url)

        players = self.game_service.get_lobby()

        self.assertEqual(2, len(players['lobby']))

    def test__create_tournament__should_add_new_tournament_to_tournaments(self):
        tournament = self.game_service.create_tournament('Fun tournament')

        self.assertEqual(1, len(self.game_service.tournaments))
        assert UUID(tournament['key'])
        self.assertEqual(0, len(tournament['rounds']))

        tournament_object = self.game_service.tournaments[UUID(tournament['key'])]
        assert tournament_object.lobby is not self.game_service.lobby

    def test__play_round__should_add_a_new_round_to_the_specified_tournament(self):
        tournament = self.game_service.create_tournament('Fun tournament')

        self.game_service.enter_lobby(self.player_x_name, self.update_url)
        self.game_service.enter_lobby('another player', self.update_url)

        x_size = 4
        y_size = 4
        winning_length = 3

        mock_scheduler = MagicMock(autospec=True)

        self.game_service.play_round(mock_scheduler,
                                     UUID(tournament['key']),
                                     x_size,
                                     y_size,
                                     winning_length)

        self.assertEqual(1, len(self.game_service.tournaments[UUID(tournament['key'])].rounds))
