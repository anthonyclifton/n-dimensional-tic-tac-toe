from marshmallow import Schema, fields

from ndimensionaltictactoe.models.mark import Mark


class PlayerXGameSchema(Schema):
    name = fields.String
    key = fields.UUID
    size_x = fields.Number
    size_y = fields.Number
    player_x_key = fields.UUID
    cells = fields.Nested(Mark)
    winning_length = fields.Number


class PlayerOGameSchema(Schema):
    name = fields.String
    key = fields.UUID
    size_x = fields.Number
    size_y = fields.Number
    player_x_key = fields.UUID
    cells = fields.Nested(Mark)
    winning_length = fields.Number
