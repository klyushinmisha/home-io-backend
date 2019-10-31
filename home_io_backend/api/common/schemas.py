__all__ = [
    'PaginationSchema'
]

from marshmallow import fields, Schema, validate


class PaginationSchema(Schema):
    page = fields.Integer(
        validate.Range(min=0)
    )

    per_page = fields.Integer(
        validate.Range(min=0)
    )


PaginationSchema = PaginationSchema()
