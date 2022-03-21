from peewee import Model, SqliteDatabase, IntegerField, DoubleField, DoesNotExist

conn = SqliteDatabase('sqlite3.db')


class BaseModel(Model):
    class Meta:
        database = conn


class Users(BaseModel):

    id = IntegerField(null=True)
    user_id = IntegerField()
    warns = IntegerField(null=True, default=0)
    muted_until = DoubleField(null=True, default=0.0)
    banned_until = DoubleField(null=True, default=0.0)

    class Meta:
        table_name = 'users'


if __name__ == '__main__':
    try:
        user = Users.get(Users.id == 1)
    except DoesNotExist:
        user = Users(user_id=1292)

    user.warns += 1
    user.save()

    print("test:", user.warns)