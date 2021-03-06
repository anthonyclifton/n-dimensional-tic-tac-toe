from marshmallow import Schema, fields


class CreateGameRequestSchema(Schema):
    game_name = fields.String()
    player_name = fields.String()
    update_url = fields.String()
    size_x = fields.Integer()
    size_y = fields.Integer()
    winning_length = fields.Integer()


class JoinGameRequestSchema(Schema):
    game_key = fields.UUID()
    player_name = fields.String()
    update_url = fields.String()


class MarkCellRequestSchema(Schema):
    game_key = fields.UUID()
    player_key = fields.UUID()
    x = fields.Integer()
    y = fields.Integer()


class LobbyRequestSchema(Schema):
    player_name = fields.String()
    update_url = fields.String()


class TournamentRequestSchema(Schema):
    tournament_name = fields.String()


class RoundRequestSchema(Schema):
    tournament_key = fields.UUID()
    x_size = fields.Integer()
    y_size = fields.Integer()
    winning_length = fields.Integer()
