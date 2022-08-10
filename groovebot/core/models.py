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
        return (
            f"***Acronym:*** `{self.acronym}`\n***Title:*** `{self.title}`\n***Album:*** `{self.album.value}`"
            f"\n***URL:*** {self.url}"
        )


class Strike(BaseModel):
    member_id = fields.CharField(max_length=18)
    reason = fields.CharField(max_length=455)
    proof = fields.CharField(max_length=455)

    def __str__(self):
        return f"***ID:*** `{self.id}`\n***Reason:*** `{self.reason}`\n***Proof:*** {self.proof}"
