from marshmallow import (
    Schema,
    fields,
    validate,
)


class InterventionPharmActionResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    intervention_id = fields.Integer(required=True)
    pharm_action_id = fields.Integer(required=True)
    updated_at = fields.DateTime()
