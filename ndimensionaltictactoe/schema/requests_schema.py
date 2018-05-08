from marshmallow import Schema, fields


class CreateGameRequestSchema(Schema):
    game_name = fields.String()
    player_name = fields.String()
    update_url = fields.String()
