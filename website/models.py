import peewee
import os
import logging
import atexit

logger = logging.getLogger(__name__)

# Local imports
from __init__ import app

if __name__ != '__main__':
    if os.path.exists('./{0}'.format(app.config['DB_NAME'])):
        DB_PATH = './{0}'.format(app.config['DB_NAME'])
    elif os.path.exists('./website/{0}'.format(app.config['DB_NAME'])):
        DB_PATH = './website/{0}'.format(app.config['DB_NAME'])
    else:
        logger.critical('database could not be located')
        # exit()
else:
    DB_PATH = './{0}'.format(app.config['DB_NAME'])

try:
    logger.debug('Database is at {}'.format(DB_PATH))
except NameError:
    db = None
else:
    db = peewee.SqliteDatabase(DB_PATH)


class BaseModel(peewee.Model):
    """ Base model with a handle to the database """
    class Meta:
        database = db


class Electricity(BaseModel):
    date = peewee.DateField()
    amount = peewee.FloatField()
    kwh = peewee.FloatField()

    def __str__(self):
        return "{} {} {}".format(self.date, self.amount, self.kwh)


class Event(BaseModel):
    date_time = peewee.DateTimeField()
    name = peewee.CharField()
    deleted = peewee.BooleanField(default=False)
    description = peewee.CharField()


class Invitee(BaseModel):
    name = peewee.CharField()
    email = peewee.CharField()
    phone_number = peewee.CharField(null=True, default=None)
    # TODO Facebook?


class EventInvitee(BaseModel):
    event = peewee.ForeignKeyField(Event)
    invitee = peewee.ForeignKeyField(Invitee)


class Todo(BaseModel):
    event = peewee.ForeignKeyField(Event, related_name='todos', null=True)
    task = peewee.CharField()
    done = peewee.BooleanField(default=False)
    deleted = peewee.BooleanField(default=False)
    date_done = peewee.DateField(null=True, default=None)
    description = peewee.CharField(default="")


class Bill(BaseModel):
    due = peewee.DateField()
    name = peewee.CharField()
    amount = peewee.FloatField()


# -----------Helper functions-----------
def before_request_handler(database=db):
    logger.debug('Opening connection to DB')
    try:
        database.connect()
    except AttributeError as e:
        logger.critical('No database defined')
        raise e
    return


def after_request_handler(database=db):
    logger.debug('Closing connection to DB')
    try:
        database.close()
    except AttributeError:
        pass
    return
atexit.register(after_request_handler, db)


def create_tables():
    before_request_handler(db)
    db.create_tables([Electricity, Event, Todo, Bill, Invitee, EventInvitee], True)
    return


if __name__ == '__main__':
    import datetime
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(name)s : %(levelname)s : %(message)s')
    before_request_handler()
    create_tables()

    def fill_tables_with_dummy_data():
        # -----Electricity-----
        Electricity(date=datetime.date.today(),
                    amount=50,
                    kwh=10).save()
        Electricity(date=datetime.date.today() - datetime.timedelta(31),
                    amount=75,
                    kwh=25).save()
        Electricity(date=datetime.date.today() - datetime.timedelta(31*2),
                    amount=66,
                    kwh=15).save()

        # -----Event-----
        event_today = Event(name="Event Today",
              date_time=datetime.datetime.today(),
              description="This date is today at the time of the creation")
        event_today.save()

        # events in the future
        Event(name="Event Tomorrow",
              date_time=datetime.datetime.today() + datetime.timedelta(1),
              description="24 hours in the future").save()

        event_tomorrow_7 = Event(name="Event Tomorrow @ 7:30",
              date_time=datetime.datetime.combine(datetime.date.today() + datetime.timedelta(1), datetime.time(19, 30)),
              description="for tomorrow that starts at 7:30 PM")
        event_tomorrow_7.save()
        Event(name="Event next week @ 11 AM",
              date_time=datetime.datetime.combine(datetime.date.today() + datetime.timedelta(7), datetime.time(11, 0)),
              description="7 days from now at 11 AM").save()
        Event(name="Event next month @ 5 PM",
              date_time=datetime.datetime.combine(datetime.date.today() + datetime.timedelta(28), datetime.time(17, 0)),
              description="28 days from now at 5 PM").save()

        # in the past
        event_yesterday = Event(name="Event Yesterday",
              date_time=datetime.datetime.today() - datetime.timedelta(1),
              description="-24 hours")
        event_yesterday.save()
        Event(name="Event Yesterday @ 6:14",
              date_time=datetime.datetime.combine(datetime.date.today() - datetime.timedelta(1), datetime.time(18, 14)),
              description="Yesterday in the evening").save()
        Event(name="Event last week",
              date_time=datetime.datetime.combine(datetime.date.today() - datetime.timedelta(8), datetime.time(14, 0)),
              description="8 days ago @ 2 PM").save()

        # -----Invitee-----
        Invitee(name="Test person 1",
                email="abc@123.com").save()
        Invitee(name="Test person 2",
                email="example@hotmail.com",
                phone_number="1-234-567-8901").save()
        Invitee(name="Test person 3",
                email="dfgdfgdfg",
                phone_number="741-2589").save()

        # -----EventInvitee-----
        EventInvitee(event=event_today, invitee=1).save()
        EventInvitee(event=event_tomorrow_7, invitee=1).save()
        EventInvitee(event=event_tomorrow_7, invitee=2).save()
        EventInvitee(event=event_tomorrow_7, invitee=3).save()
        EventInvitee(event=event_yesterday, invitee=3).save()

        # -----Todos-----
        Todo(task="Non event task 1").save()
        Todo(task="Second non event todo",
             description="This one has a description").save()
        Todo(task="Non event todo that's done",
             description="Todo done",
             done=True,
             date_done=datetime.date.today()).save()
        Todo(task="Non event todo that's done 4 days ago",
             description="Todo done 4 days ago",
             done=True,
             date_done=datetime.date.today() - datetime.timedelta(4)).save()
        Todo(task="Non event todo that's done 7 days ago",
             description="Todo done 4 days ago",
             done=True,
             date_done=datetime.date.today() - datetime.timedelta(7)).save()
        Todo(task="Non event todo that's done 8 days ago",
             description="Todo finished 8 days ago",
             done=True,
             date_done=datetime.date.today() - datetime.timedelta(8)).save()

        Todo(task="Event1 task1",
             event=event_today).save()
        Todo(task="Event1 task2",
             event=event_today,
             description="Event 1 task 2").save()
        Todo(task="Event3 task1",
             event=event_tomorrow_7,
             description="Event 3 task 1").save()
        Todo(task="Event3 task2",
             event=event_tomorrow_7).save()
        Todo(task="Event yesterday task",
             event=event_yesterday).save()

        # -----Bill-----
        Bill(due=datetime.date.today(),
             name="Electricity",
             amount="66.34").save()
        Bill(due=datetime.date.today() + datetime.timedelta(3),
             name="Water",
             amount="25").save()
        Bill(due=datetime.date.today() - datetime.timedelta(3),
             name="Past Bill",
             amount="123").save()

        return
