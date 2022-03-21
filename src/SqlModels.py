from peewee import Model, SqliteDatabase, IntegerField, DoubleField, DoesNotExist


class Users(Model):

    id = IntegerField(null=True)
    user_id = IntegerField()
    warns = IntegerField(null=True, default=0)
    muted_until = DoubleField(null=True, default=0.0)
    banned_until = DoubleField(null=True, default=0.0)

    class Meta:
        table_name = 'users'
        database = SqliteDatabase('sqlite3.db')
