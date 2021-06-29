from tortoise import Model, fields


class User(Model):
    name = fields.CharField(max_length=20)
    password = fields.CharField(max_length=200)
    age = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
