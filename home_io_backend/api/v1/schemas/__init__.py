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

    # device task schemas
    'DeviceTaskReadSchema',
    'DeviceTasksReadSchema',
    'DeviceTaskCreateSchema',
    'DeviceTasksCreateSchema',
    'DeviceTaskUpdateSchema'
]


from .device import DeviceSchema
from .device_log import DeviceLogSchema
from .device_task import DeviceTaskSchema
from .user import UserSchema


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
    exclude=('id', 'registered_at', )
)
DeviceUpdateSchema = DeviceSchema(
    exclude=('id', 'registered_at', 'owner_id'),
    partial=True
)

DeviceLogReadSchema = DeviceLogSchema()
DeviceLogsReadSchema = DeviceLogSchema(many=True)
DeviceLogCreateSchema = DeviceLogSchema(
    exclude=('id', 'created_at')
)
DeviceLogsCreateSchema = DeviceLogSchema(
    exclude=('id', 'created_at'),
    many=True
)
DeviceLogUpdateSchema = DeviceLogSchema(
    exclude=('id', 'created_at'),
    partial=True
)

DeviceTaskReadSchema = DeviceTaskSchema()
DeviceTasksReadSchema = DeviceTaskSchema(many=True)
DeviceTaskCreateSchema = DeviceTaskSchema(
    exclude=('id', 'created_at')
)
DeviceTasksCreateSchema = DeviceTaskSchema(
    exclude=('id', 'created_at'),
    many=True
)
DeviceTaskUpdateSchema = DeviceTaskSchema(
    exclude=('id', 'created_at'),
    partial=True
)
