import os
from enum import Enum

from tortoise import Tortoise, exceptions, fields
from tortoise.models import Model, Q


DATABASE = "polaris"
DATABASE_URL = (
    f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{DATABASE}?charset=utf8mb4"
)


class IntegrationType(str, Enum):
    Discord = "Discord"


async def init():
    await Tortoise.init(
        {
            "connections": {DATABASE: DATABASE_URL},
            "apps": {
                DATABASE: {
                    "models": [__name__],
                    "default_connection": DATABASE,
                }
            },
        },
    )
    await Tortoise.generate_schemas(safe=True)
    print(f"Database {DATABASE} initialized")


class Team(Model):
    team_id = fields.UUIDField(pk=True)
    icon_url = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=64)
    owner = fields.ForeignKeyField(
        f"{DATABASE}.User",
        to_field="user_id",
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "teams"


class TeamMember(Model):
    member_id = fields.UUIDField(pk=True)
    joined_at = fields.DatetimeField(auto_now_add=True)
    team = fields.ForeignKeyField(
        f"{DATABASE}.Team",
        to_field="team_id",
        on_delete=fields.CASCADE,  # TODO ask chatgpt how this shit works
    )
    user = fields.ForeignKeyField(
        f"{DATABASE}.User",
        to_field="user_id",
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "team_members"


class Agent(Model):
    agent_id = fields.UUIDField(pk=True)
    owner = fields.ForeignKeyField(
        f"{DATABASE}.User",
        to_field="user_id",
        on_delete=fields.CASCADE,
    )
    team = fields.ForeignKeyField(
        f"{DATABASE}.Team",
        to_field="team_id",
        on_delete=fields.CASCADE,
    )
    name = fields.CharField(max_length=255)
    token = fields.TextField()
    type = fields.CharEnumField(IntegrationType)
    account_id = fields.BigIntField()

    class Meta:
        table = "agents"


class User(Model):
    user_id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, null=True)
    salt = fields.CharField(max_length=255)
    hash = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    totp = fields.CharField(max_length=255, null=True)
    ips = fields.JSONField(null=True)
    totp = fields.CharField(max_length=255, null=True)
    icon_url = fields.CharField(max_length=255, null=True)
    extra = {}

    class Meta:
        table = "users"

    @classmethod
    async def auth_user(cls, user, password):
        assert user is not None, HTTPException(400, "'user' param is missing")
        assert password is not None, HTTPException(
            400, "'password' param is missing")
        try:
            user = await cls.get(Q(username=user) | Q(email=user))
        except (exceptions.MultipleObjectsReturned, exceptions.DoesNotExist):
            raise HTTPException(401, "Invalid credentials")
        if not user.verify_password(password):
            raise HTTPException(401, "Invalid credentials")
        return user

    def to_token(self, **extra):
        data = {"user_id": str(self.user_id), "salt": self.salt}
        return cipher.encrypt({**extra, **data})

    @classmethod
    async def from_token(cls, token) -> "User":
        data: dict = cipher.decrypt(token)
        if data is None:
            raise HTTPException(401, "Invalid Authorization")
        try:
            user_id = data.get("user_id")
            user: User = await cls.get(user_id=user_id)
        except (exceptions.MultipleObjectsReturned, exceptions.DoesNotExist):
            raise HTTPException(401, "Invalid Authorization")
        user.extra = data
        return user

    def verify_password(self, password):
        hash_stored = self.hash
        hash = cipher.hash(password + self.salt)
        return hash_stored == hash


class View(Model):
    view_id = fields.UUIDField(pk=True)
    integrated_id = fields.BigIntField(null=True)
    user_id = fields.BigIntField()
    agent = fields.ForeignKeyField(
        f"{DATABASE}.Agent",
        to_field="agent_id",
        on_delete=fields.CASCADE,
    )
    view_group = fields.ForeignKeyField(
        f"{DATABASE}.ViewGroup",
        to_field="view_group_id",
        on_delete=fields.CASCADE,
    )
    name = fields.CharField(max_length=255)
    whitelist = fields.BooleanField(default=False)
    type = fields.CharEnumField(IntegrationType)
    #
    token = None

    class Meta:
        table = "views"


class ViewGroup(Model):
    view_group_id = fields.UUIDField(pk=True)
    team = fields.ForeignKeyField(
        f"{DATABASE}.Team",
        to_field="team_id",
        on_delete=fields.CASCADE,
    )
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "view_groups"
