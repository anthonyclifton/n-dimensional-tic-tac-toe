from marshmallow import Schema, fields


class GridIdentifiersSchema(Schema):
    grid_key = fields.UUID
    x_user_key = fields.UUID
    o_user_key = fields.UUID
