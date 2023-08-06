"""Declares :class:`ReadmeSchema`."""
import marshmallow
import marshmallow.fields

from .readmeexample import ReadmeExampleSchema


class ReadmeSchema(marshmallow.Schema):
    examples = marshmallow.fields.List(
        marshmallow.fields.Nested(ReadmeExampleSchema),
        missing=None,
        required=False
    )
