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
        game_result = "drew"
        if game.player_x.winner:
            game_result = "won"
        elif game.player_o.winner:
            game_result = "lost"

        print "{} (Player X) {} Game {} with {} (Player O)".format(game.player_x.name,
                                                                   game_result,
                                                                   game.name,
                                                                   game.player_o.name)

    print ""
    for player_key in round.scoreboard:
        player_name = lobby[player_key].name
        score = str(round.scoreboard[player_key])
        print "{}: {} points".format(player_name, score)

    print "{}".format("-" * 80)


def render_tournament_outcome(tournament):
    tournament_name = tournament.name[:30]
    title_bar_length = 80 - (len(tournament_name) + 29)
    print ""
    print "----[ Tournament Complete: {} ]{}".format(tournament_name, "-" * title_bar_length)

    print "Rounds Played: {}".format(len(tournament.rounds))

    for player_key in tournament.lobby:
        player_name = tournament.lobby[player_key].name
        total_points = sum([round.scoreboard[player_key] for round in tournament.rounds])

        print "{} had {} wins, {} losses, and {} draws with {} total points".format(player_name,
                                                                                    'X',
                                                                                    'Y',
                                                                                    'Z',
                                                                                    total_points)
    print "{}".format("-" * 80)
