from ndimensionaltictactoe.models.mark import X_MARK, O_MARK


def render_game_outcome(game):
    game_name = game.name[:30]
    title_bar_length = 80 - (len(game_name) + 23)
    player_x_moves = len([move for move in game.cells if move.value == X_MARK])
    player_o_moves = len([move for move in game.cells if move.value == O_MARK])

    print ""
    print "----[ Game Complete: {} ]{}".format(game_name, "-" * title_bar_length)
    print "{} (Player X) made {} moves".format(game.player_x.name[:30], player_x_moves)
    print "{} (Player O) made {} moves\n".format(game.player_o.name[:30], player_o_moves)
    if game.player_x.winner:
        print("Winner: Player X")
    elif game.player_o.winner:
        print("Winner: Player O")
    else:
        print("Game was Drawn")
    print "{}".format("-" * 80)


def render_round_outcome(tournament_name, round, round_number, lobby):
    round_name = "Round #{}".format(round_number)
    title_bar_length = 80 - (len(round_name) + len(tournament_name) + 33)
    print ""
    print "----[ {} Complete in Tournament: {} ]{}".format(round_name,
                                                           tournament_name,
                                                           "-" * title_bar_length)

    print "{}".format("-" * 80)
