from marshmallow import Schema, fields


class MarkSchema(Schema):
    x = fields.Integer()
    y = fields.Integer()
    value = fields.Integer()


class PlayerSchema(Schema):
    key = fields.UUID()
    name = fields.String()
    winner = fields.Boolean()


class PlayerSummarySchema(Schema):
    name = fields.String()


class PlayerXGameSchema(Schema):
    name = fields.String()
    key = fields.UUID()
    size_x = fields.Integer()
    size_y = fields.Integer()
    player_x = fields.Nested(PlayerSchema)
    cells = fields.Nested(MarkSchema, many=True)
    winning_length = fields.Integer()
    state = fields.Integer()
    winner = fields.Boolean()


class PlayerOGameSchema(Schema):
    name = fields.String()
    key = fields.UUID()
    size_x = fields.Integer()
    size_y = fields.Integer()
    player_o = fields.Nested(PlayerSchema)
    cells = fields.Nested(MarkSchema, many=True)
    winning_length = fields.Integer()
    state = fields.Integer()
    winner = fields.Boolean()


class GameSummarySchema(Schema):
    name = fields.String()
    key = fields.UUID()
    size_x = fields.Integer()
    size_y = fields.Integer()
    winning_length = fields.Integer()
    player_x = fields.Nested(PlayerSummarySchema)
    player_o = fields.Nested(PlayerSummarySchema)
