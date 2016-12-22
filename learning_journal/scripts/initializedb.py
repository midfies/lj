import os
import sys
import transaction
import datetime

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import Entry


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        ENTRIES = [
            {"title": "First Entry", "creation_date": datetime.datetime(2016, 12, 18, 0, 0), "body": "This is a fake learning journal thay I did not write but I wanted to have at least three examples in the entries list..", "category": "Testing", "tags": "Testing"},
            {"title": "LJ - Day 11", "creation_date": datetime.datetime(2016, 12, 19, 0, 0), "body": "Today is class we started learning about pyramid and how to build an app using this framework. We are also continuing on in our data structures assignment and I have changed to be partners with Marc K. This was interesting in working on our deque for the day since we started with his data-structure repo so I had to learn a bit about how they named and formated their doubly linked list. There is also a difference in how we approach the testing. This should  be a good learning experience as we continue to work together.", "category": "Learning Journal", "tags": "Learning Journal"},
            {"title": "LJ - Day 12", "creation_date": datetime.datetime(2016, 12, 20, 0, 0), "body": "Well there was a ton of stuff covered in class today and none of it is crazy but Im definitly not retaining all of it.  Still way too much of a workload in this class and I am starting to get way to pissed off at anything and everything.  I left early after struggling through the binary heap with Marc.  I stressed my way all the way to the bus and even yelled at a lady for blatantly littering on the ground.  I went to my parents place where I was able to see my nephew who is two years old and lives in South Carolina.  He is so close to spitting out full on sentances and it was amazing to get to feel joy for the first time in a few weeks.  I also got to see my younger brother and his wife which was amazing and I truely miss them since they live on the other side of the country.  After spending a little while with my family I returned to the misery that is this worhtless pile of assignments that is apparently not actually meant to be accomplished each day.  This place is just a game and seems like a waste of my time more often than not now.  So all in all today I learned that my family will always be more important than some class and I also learned that I can still feel terrible for screwing over my partner and leaving early", "category": "Learning Journal", "tags": "Learning Journal"},

        ]

        for entry in ENTRIES:
            new_entry = Entry(title=entry['title'], body=entry['body'], creation_date=entry['creation_date'], category=entry['category'], tags=entry['tags'])

            dbsession.add(new_entry)

