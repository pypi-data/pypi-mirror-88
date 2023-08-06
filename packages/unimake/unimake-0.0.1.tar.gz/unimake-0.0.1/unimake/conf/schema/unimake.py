"""Declares :class:`UnimakeSchema`."""
import marshmallow
import marshmallow.fields
from unimatrix.lib.datastructures import ImmutableDTO

from .project import ProjectSchema
from .readme import ReadmeSchema


class UnimakeSchema(marshmallow.Schema):
    dict_class = ImmutableDTO

    project = marshmallow.fields.Nested(
        ProjectSchema,
        required=True
    )

    readme = marshmallow.fields.Nested(
        ReadmeSchema,
        required=True
    )
