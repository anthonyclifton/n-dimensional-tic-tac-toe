from marshmallow import Schema, fields


class CreateGameRequestSchema(Schema):
    game_name = fields.String()
    player_name = fields.String()
    update_url = fields.String()


class JoinGameRequestSchema(Schema):
    game_key = fields.UUID()
    player_name = fields.String()
    update_url = fields.String()


class MarkCellRequestSchema(Schema):
    game_key = fields.UUID()
    player_key = fields.UUID()
    x = fields.Number()
    y = fields.Number()