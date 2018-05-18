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

    print "Board Size: {} cells by {} cells".format(round.x_size, round.y_size)
    print "Winning Line Length: {} cells".format(round.winning_length)
    print "Winners Receive: {} points (points split on draw)\n".format(round.winner_points)

    for game in round.games:
        print "{} Player {} {} Game {} with {} Player {}".format("bob",
                                                                 "X",
                                                                 "won",
                                                                 "game1",
                                                                 "joe",
                                                                 "O")

    for score in round.scoreboard:
        print "{}:{}{} points".format("bob", " " * 5, "16")

    print "{}".format("-" * 80)
