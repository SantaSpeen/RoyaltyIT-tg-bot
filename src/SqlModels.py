from peewee import Model, SqliteDatabase, IntegerField, DoubleField, BooleanField, TextField


class BasicModel(Model):
    class Meta:
        database = SqliteDatabase('sqlite3.db')


class Users(BasicModel):

    id = IntegerField(null=True)
    user_id = IntegerField()
    warns = IntegerField(null=True, default=0)
    muted_until = DoubleField(null=True, default=0.0)
    banned = BooleanField(null=True, default=False)
    ban_by = IntegerField(null=True)
    ban_msg = TextField(null=True)

    class Meta:
        table_name = 'users'


class Mailing(BasicModel):

    id = IntegerField(null=True)
    user_id = IntegerField()
    enable = BooleanField(null=True, default=True)

    class Meta:
        table_name = 'mailing'
