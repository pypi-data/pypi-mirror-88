"""Declares :class:`ProjectSchema`."""
import marshmallow
import marshmallow.fields


class ProjectSchema(marshmallow.Schema):
    kind = marshmallow.fields.String(
        validate=marshmallow.validate.OneOf(['library', 'application']),
        required=True
    )
    title = marshmallow.fields.String(
        required=True
    )

    description = marshmallow.fields.String(
        required=True
    )
