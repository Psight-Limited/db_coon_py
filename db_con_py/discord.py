import os

from tortoise import Tortoise, fields
from tortoise.models import Model


DATABASE = "discord"
DATABASE_URL = (
    f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{DATABASE}?charset=utf8mb4"
)


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
        }
    )
    await Tortoise.generate_schemas(safe=True)
    print(f"Database {DATABASE} initialized")


class Starboard(Model):
    id = fields.UUIDField(pk=True)
    sb_channel = fields.BigIntField()
    og_channel = fields.BigIntField()
    sb_message_id = fields.BigIntField()
    og_message_id = fields.BigIntField()

    class Meta:
        table = "starboard"


class User(Model):
    id = fields.BigIntField(pk=True, generated=False)
    kartra_email = fields.CharField(max_length=254, null=True)
    discord_id = fields.BigIntField(null=True)
    journeyman = fields.BooleanField(null=True)
    acolyte = fields.BooleanField(null=True)
    type = fields.CharField(max_length=4, null=True)
    octagram = fields.CharField(max_length=4, null=True)
    type_secret = fields.CharField(max_length=4, null=True)
    octagram_secret = fields.CharField(max_length=4, null=True)
    ignore_data = fields.BooleanField(default=False)

    class Meta:
        table = "users"


class DiscordUser(Model):
    id = fields.BigIntField(pk=True, generated=False)
    username = fields.TextField()
    avatar = fields.TextField(null=True)
    discriminator = fields.TextField()
    public_flags = fields.IntField(null=True)
    flags = fields.IntField(null=True)
    banner = fields.TextField(null=True)
    accent_color = fields.IntField(null=True)
    global_name = fields.TextField(null=True)
    avatar_decoration = fields.TextField(null=True)
    display_name = fields.TextField(null=True)
    banner_color = fields.TextField(null=True)
    last_updated = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "discord_users"


class DiscordMember(Model):
    id = fields.UUIDField(pk=True)
    guild_id = fields.BigIntField()
    user: DiscordUser = fields.ForeignKeyField(
        f"{DATABASE}.DiscordUser",
        to_field="id",
    )
    avatar = fields.TextField(null=True)
    communication_disabled_until = fields.DatetimeField(null=True)
    flags = fields.IntField(null=True)
    is_pending = fields.BooleanField(null=True)
    joined_at = fields.DatetimeField(null=True)
    nick = fields.TextField(null=True)
    pending = fields.BooleanField(null=True)
    premium_since = fields.DatetimeField(null=True)
    roles = fields.JSONField(null=True)
    mute = fields.BooleanField(null=True)
    deaf = fields.BooleanField(null=True)
    last_updated = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "discord_members"


class Queued(Model):
    id = fields.IntField(pk=True)

    class Meta:
        table = "queued"


class Message(Model):
    guild_id = fields.BigIntField()
    channel_id = fields.BigIntField(index=True)
    bucket = fields.IntField(index=True)
    message_id = fields.BigIntField(index=True, unique=True, pk=True)
    created_at = fields.DatetimeField()
    author_id = fields.BigIntField()
    content = fields.TextField(null=True)
    reference_id = fields.BigIntField(null=True)

    class Meta:
        table = "messages"


class TestV1Submissions(Model):
    discord_id = fields.BigIntField(index=True)
    submitted = fields.JSONField()
    timestamp = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "test_v1_submissions"
