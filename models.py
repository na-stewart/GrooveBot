from os import environ

from tortoise import Model, fields


class BaseModel(Model):
    id = fields.IntField(pk=True)
    date_created = fields.DatetimeField(auto_now_add=True)
    date_updated = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class Album(BaseModel):
    acronym = fields.CharField(max_length=12, unique=True)
    title = fields.CharField(max_length=455)
    description = fields.TextField()

    def __str__(self):
        return f"***Acronym:*** `{self.acronym}`\n***Title:*** `{self.title}`\n***Description:*** `{self.description}`"


class Music(BaseModel):
    acronym = fields.CharField(max_length=12, unique=True)
    title = fields.CharField(max_length=455)
    album = fields.ForeignKeyField("models.Album", null=True)
    url = fields.CharField(max_length=455, null=True)

    def __str__(self):
        model_str = f"***Acronym:*** `{self.acronym}`\n***Title:*** `{self.title}`\n"
        if self.url:
            model_str += f"***URL:*** {self.url}"
        return model_str


class Strike(BaseModel):
    member_id = fields.CharField(max_length=18)
    reason = fields.CharField(max_length=455)
    proof = fields.CharField(max_length=455)

    def __str__(self):
        return f"***ID:*** `{self.id}`\n***Reason:*** `{self.reason}`\n***Proof:*** {self.proof}"


class Config(dict):
    TOKEN: str
    WELCOME_MESSAGE: str
    DATABASE_URL: str
    WELCOME_CHANNEL_ID: str
    VERIFICATION_CHANNEL_ID: str
    VERIFIED_ROLE_ID: str

    def load_environment_variables(self, load_env="GROOVEBOT_") -> None:
        """
        Any environment variables defined with the prefix argument will be applied to the config.
        Args:
            load_env (str): Prefix being used to apply environment variables into the config.
        """
        for key, value in environ.items():
            if not key.startswith(load_env):
                continue
            _, config_key = key.split(load_env, 1)
            self[config_key] = str(value)

    def __init__(self, default_config: dict):
        super().__init__(default_config)
        self.__dict__ = self
        self.load_environment_variables()
