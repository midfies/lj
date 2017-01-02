"""Tests for the learning journal web app."""

import pytest
import transaction
import datetime

from pyramid import testing
from pyramid.config import Configurator

from learning_journal.models import (
    Entry,
    get_tm_session,
)
from learning_journal.models.meta import Base

TEST_ENTRIES = [
    {'title': "Testing Models",
     'body': 'This is just a test. This is the 1st Entry',
     'category': 'testing1',
     'creation_date': datetime.datetime(2016, 12, 30, 0, 0),
     'tags': 'test testing'},
    {'title': "Testing Models 2",
     'body': 'This is just a test. This is the 2nd Entry',
     'category': 'testing1',
     'creation_date': datetime.datetime(2016, 12, 30, 0, 0),
     'tags': 'test'},
    {'title': "Testing Models 3",
     'body': 'This is just a test. This is the 3rd Entry',
     'category': 'testing2',
     'creation_date': datetime.datetime(2016, 12, 30, 0, 0),
     'tags': 'testing'},
    {'title': "Testing Models 4",
     'body': 'This is just a test. This is the 4th Entry',
     'category': 'testing2',
     'creation_date': datetime.datetime(2016, 12, 30, 0, 0),
     'tags': 'test'},
    {'title': "Testing Models 5",
     'body': 'This is just a test. This is the 5th Entry',
     'category': 'testing2',
     'creation_date': datetime.datetime(2016, 12, 30, 0, 0),
     'tags': 'testing'},
]


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.

    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://midfies:password@localhost:5432/test_lj'
    })
    config.include("learning_journal.models")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture(scope="function")
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    session_factory = configuration.registry["dbsession_factory"]
    session = session_factory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_posts(dummy_request):
    """Add multiple entries to the database."""
    for entry in TEST_ENTRIES:
            post = Entry(title=entry['title'], body=entry['body'], category=entry['category'], creation_date=entry['creation_date'], tags=entry['tags'])
            dummy_request.dbsession.add(post)


@pytest.fixture(scope="function")
def testapp():
    from webtest import TestApp

    def main(global_config, **settings):
        """This function returns a Pyramid WSGI application."""
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('learning_journal.models')
        config.include('learning_journal.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main({}, **{
        'sqlalchemy.url': 'postgres://midfies:password@localhost:5432/test_lj'
    })

    testapp = TestApp(app)
    session_factory = app.registry["dbsession_factory"]
    session = session_factory()
    engine = session.bind
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)

    return testapp


@pytest.fixture
def fill_the_db(testapp):
    session_factory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        for entry in TEST_ENTRIES:
            post = Entry(title=entry['title'], body=entry['body'], category=entry['category'], creation_date=entry['creation_date'], tags=entry['tags'])
            dbsession.add(post)
    return dbsession

# Unit Tests


def test_model_gets_added(db_session):
    """Test that adding a model to the DB actually does so."""
    assert len(db_session.query(Entry).all()) == 0
    model = Entry(title="Testing Models", body='This is just a test', category='testing', creation_date=datetime.datetime(2016, 12, 18, 0, 0), tags='test testing')
    db_session.add(model)
    assert len(db_session.query(Entry).all()) == 1


def test_list_view_returns_entries_from_db(dummy_request, add_posts):
    """Test that the list view returns entries from DB."""
    from learning_journal.views.default import list_view
    result = list_view(dummy_request)
    assert result['entries'][0].title == "Testing Models"
    assert result['entries'][1].category == "testing1"
    assert len(result['entries']) == 5


# Functional Tests

def test_layout_root(testapp):
    """Test that the contents of the root page contains <article>."""
    response = testapp.get('/', status=200)
    html = response.html
    assert 'Marc Fieser' in html.find("footer").text


def test_create_view_contains_a_form(testapp):
    """Doc."""
    response = testapp.get('/journal/new-entry', status=200)
    html = response.html
    assert len(html.find_all("form")) == 1


def test_about_me_contains_info(testapp):
    """Test that the about me page has content."""
    response = testapp.get('/about')
    html = response.html
    assert 'About Me' in html.find('h1').text


def test_create_view_redirects(testapp):
    """Test that a create view redirects."""
    post_params = {'title': 'Test', 'body': 'body', 'category': 'testing', 'tags': ''}
    response = testapp.post('/journal/new-entry', post_params, status=302)
    assert response.status == '302 Found'


def test_root_contents(testapp):
    """Test that there are no entries on the page."""
    fill_the_db(testapp)
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.findAll("article")) == 5


def test_detail_view_shows_correct_entry(testapp):
    """Test that detail view shows the correct entry."""
    fill_the_db(testapp)
    response = testapp.get('/journal/2', status=200)
    html = response.html
    assert 'Testing Models 2' in html.text


def test_category_view_display_correct_amount(testapp):
    """Test that category view displays all of specific category."""
    fill_the_db(testapp)
    response = testapp.get('/journal/category/testing1', status=200)
    html = response.html
    assert len(html.findAll('article')) == 2
