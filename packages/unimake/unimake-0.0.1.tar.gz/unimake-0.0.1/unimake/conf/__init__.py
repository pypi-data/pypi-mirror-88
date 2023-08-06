"""Exposes the Unimake configuration for a project."""
import yaml

from .schema import UnimakeSchema


schema = UnimakeSchema()
with open('.unimake.yml') as f:
    settings = schema.load(yaml.safe_load(f.read()))
