from marshmallow import Schema,fields


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainItemsSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    
class ItemsUpdateSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class ItemsSchema(PlainItemsSchema):
    store_id = fields.Int(required=True,load_only=True)
    stores = fields.Nested(PlainStoreSchema(),dump_only=True)
    
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemsSchema()), dump_only=True)
    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username=fields.Str(required=True)
    password=fields.Str(required=True,load_only=True)
    role = fields.Str(dump_only=True,load_only=True,default="user")