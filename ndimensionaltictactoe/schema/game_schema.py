from marshmallow import Schema, fields
from marshmallow.fields import Field


class MarkSchema(Schema):
    x = fields.Number()
    y = fields.Number()
    value = fields.Number()


class PlayerSchema(Schema):
    key = fields.UUID()
    name = fields.String()


class PlayerSummarySchema(Schema):
    name = fields.String()


class PlayerXGameSchema(Schema):
    name = fields.String()
    key = fields.UUID()
    size_x = fields.Number()
    size_y = fields.Number()
    player_x = fields.Nested(PlayerSchema)
    cells = fields.Nested(MarkSchema, many=True)
    winning_length = fields.Number()
    state = fields.Integer()


class PlayerOGameSchema(Schema):
    name = fields.String()
    key = fields.UUID()
    size_x = fields.Number()
    size_y = fields.Number()
    player_o = fields.Nested(PlayerSchema)
    cells = fields.Nested(MarkSchema, many=True)
    winning_length = fields.Number()
    state = fields.Integer()


class GameSummarySchema(Schema):
    name = fields.String()
    key = fields.UUID()
    size_x = fields.Number()
    size_y = fields.Number()
    winning_length = fields.Number()
    player_x = fields.Nested(PlayerSummarySchema)
    player_o = fields.Nested(PlayerSummarySchema)
