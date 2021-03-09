import uuid

from tortoise import Model, fields


class BaseModel(Model):
    id = fields.IntField(pk=True)
    uid = fields.UUIDField(default=uuid.uuid1, max_length=36)
    parent_uid = fields.UUIDField(null=True, max_length=36)
    date_created = fields.DatetimeField(auto_now_add=True)
    date_updated = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class Abbreviation(BaseModel):
    acronym = fields.CharField(max_length=12, unique=True)
    value = fields.CharField(max_length=45)

    def __str__(self):
        return f"***Acronym:*** `{self.acronym}`\n***Value:*** `{self.value}`"


class Album(Abbreviation):
    description = fields.TextField()

    def __str__(self):
        return f"***Acronym:*** `{self.acronym}`\n***Title:*** `{self.value}`\n***Description:*** `{self.description}`"


class Music(Abbreviation):
    url = fields.CharField(max_length=45)

    def __str__(self):
        return f"***Acronym:*** `{self.acronym}`\n***Title:*** `{self.value}`\n***URL:*** {self.url}"


class Strike(BaseModel):
    member_id = fields.CharField(max_length=18)
    reason = fields.CharField(max_length=45)

    def __str__(self):
        return f"***Date*** `{str(self.date_created).split(' ')[0]}`\n***Number:*** `{self.id}`\n***Reason:*** " \
               f"`{self.reason}`"
