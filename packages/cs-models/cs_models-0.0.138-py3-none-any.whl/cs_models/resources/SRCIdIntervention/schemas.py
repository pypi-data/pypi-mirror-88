from marshmallow import (
    Schema,
    fields,
    validate,
)


class SRCIdInterventionResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    src_id = fields.String(validate=not_blank, required=True)
    src_type = fields.String(validate=not_blank, required=True)
    intervention_id = fields.Integer(required=True)
    narrow = fields.Boolean(required=True)
    group = fields.Integer(required=True)
    updated_at = fields.DateTime()
