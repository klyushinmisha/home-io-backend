def create_instance(schema, json):
    data = schema.load(json)
    return schema.model(**data)


def update_instance(schema, json, obj):
    data = schema.load(json)
    for k, v in proc_data:
        setattr(obj, k, v)
    return schema.model(**data)


from .user import UserSchema
from .device import DeviceSchema
from .device_log import DeviceLogSchema


UserReadSchema = UserSchema()
UsersReadSchema = UserSchema(many=True)
UserCreateSchema = UserSchema(
    exclude=('id', 'created_at', 'devices')
)
UserUpdateSchema = UserSchema(
    exclude=('id', 'created_at', 'devices'),
    partial=True
)

DeviceReadSchema = DeviceSchema()
DevicesReadSchema = DeviceSchema(many=True)
DeviceCreateSchema = DeviceSchema(
    exclude=('id', 'registred_at','owner_id')
)
DeviceUpdateSchema = DeviceSchema(
    exclude=('id', 'registred_at', 'owner_id'),
    partial=True
)

DeviceLogReadSchema = DeviceLogSchema()
DeviceLogsReadSchema = DeviceLogSchema(many=True)
DeviceLogCreateSchema = DeviceLogSchema(
    exclude=('id', 'created_at', 'device_id')
)
DeviceLogsCreateSchema = DeviceLogSchema(
    exclude=('id', 'created_at', 'device_id'),
    many=True
)
DeviceLogUpdateSchema = DeviceLogSchema(
    exclude=('id', 'created_at', 'device_id'),
    partial=True
)


__all__ = [
    # user schemas
    'UserReadSchema',
    'UsersReadSchema',
    'UserCreateSchema',
    'UserUpdateSchema',

    # device schemas
    'DeviceReadSchema',
    'DevicesReadSchema',
    'DeviceCreateSchema',
    'DeviceUpdateSchema',

    # device log schemas
    'DeviceLogReadSchema',
    'DeviceLogsReadSchema',
    'DeviceLogCreateSchema',
    'DeviceLogsCreateSchema',
    'DeviceLogUpdateSchema',
]
