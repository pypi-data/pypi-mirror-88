from marshmallow import (
    Schema,
    fields,
    validate,
)


class SRCIdConditionResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    src_id = fields.String(validate=not_blank, required=True)
    src_type = fields.String(validate=not_blank, required=True)
    condition_id = fields.Integer(required=True)
    updated_at = fields.DateTime()
