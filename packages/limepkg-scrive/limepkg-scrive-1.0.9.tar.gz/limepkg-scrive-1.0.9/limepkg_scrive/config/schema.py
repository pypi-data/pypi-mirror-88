from marshmallow import Schema, fields


def create_schema(application):
    class ConfigSchema(Schema):
        scriveHost = fields.Str(default="https://lime.scrive.com")

    return ConfigSchema()
