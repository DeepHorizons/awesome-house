import peewee
import datetime
import os
import logging

logger = logging.getLogger(__name__)

DB_NAME = 'database.db'

if os.path.exists('./{0}'.format(DB_NAME)):
    DB_PATH = './{0}'.format(DB_NAME)
elif os.path.exists('./website/{0}'.format(DB_NAME)):
    DB_PATH = './website/{0}'.format(DB_NAME)
else:
    logger.critical('database could not be located')
    exit()

logger.debug('Database is at {}'.format(DB_PATH))
db = peewee.SqliteDatabase(DB_PATH)

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Electricity(BaseModel):
    date = peewee.DateField()
    amount = peewee.FloatField()
    kwh = peewee.FloatField()

    def __str__(self):
        return "{} {} {}".format(self.date, self.amount, self.kwh)

