"""Declares :class:`ReadmeExampleSchema`."""
import marshmallow
import marshmallow.fields


class ReadmeExampleSchema(marshmallow.Schema):
    name = marshmallow.fields.String(
        required=True
    )

    description = marshmallow.fields.String(
        required=False,
        missing=None
    )

    content = marshmallow.fields.String(
        required=True
    )

    language = marshmallow.fields.String(
        required=False,
        missing='',
        default=''
    )
