from marshmallow import Schema, fields


class MarkSchema(Schema):
    coordinates = fields.Number(many=True)
    value = fields.Number()


class PlayerSchema(Schema):
    key = fields.UUID()
    name = fields.String()


class PlayerXGameSchema(Schema):
    name = fields.String()
    key = fields.UUID()
    size_x = fields.Number()
    size_y = fields.Number()
    player_x = fields.Nested(PlayerSchema)
    cells = fields.Nested(MarkSchema, many=True)
    winning_length = fields.Number()


class PlayerOGameSchema(Schema):
    name = fields.String
    key = fields.UUID
    size_x = fields.Number
    size_y = fields.Number
    player_o = fields.Nested(PlayerSchema)
    cells = fields.Nested(MarkSchema, many=True)
    winning_length = fields.Number
