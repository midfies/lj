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
    {'title': "Testing Models 1",
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
    config.include("learning_journal.routes")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
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
    """Return a dummy request for testing."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_posts(dummy_request):
    """Add multiple entries to the database."""
    for entry in TEST_ENTRIES:
            post = Entry(title=entry['title'], body=entry['body'], category=entry['category'], creation_date=entry['creation_date'], tags=entry['tags'])
            dummy_request.dbsession.add(post)


@pytest.fixture
def set_auth_credentials():
    """Make a username/password combo for testing."""
    import os
    from passlib.apps import custom_app_context as pwd_context

    os.environ["AUTH_USERNAME"] = "testme"
    os.environ["AUTH_PASSWORD"] = pwd_context.hash("foobar")




# Unit Tests


# def test_model_gets_added(db_session):
#     """Test that adding a model to the DB actually does so."""
#     assert len(db_session.query(Entry).all()) == 0
#     model = Entry(title="Testing Models", body='This is just a test', category='testing', creation_date=datetime.datetime(2016, 12, 18, 0, 0), tags='test testing')
#     db_session.add(model)
#     assert len(db_session.query(Entry).all()) == 1


def test_list_view_is_empty_when_no_models(dummy_request):
    """Test there are no listings when db is empty."""
    from learning_journal.views.default import list_view
    result = list_view(dummy_request)
    assert len(result['entries']) == 0


def test_list_view_returns_entries_from_db(dummy_request, add_posts):
    """Test that the list view returns entries from DB."""
    from learning_journal.views.default import list_view
    result = list_view(dummy_request)
    assert result['entries'][0].title == "Testing Models 1"
    assert result['entries'][1].category == "testing1"
    assert len(result['entries']) == 5


def test_detail_view_displays_post(dummy_request, add_posts):
    """Test detail view displays post that is passed through url."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = '6'
    result = detail_view(dummy_request)
    entry = dummy_request.dbsession.query(Entry).get(6)
    assert result['entry'] == entry


def test_detail_view_of_non_existant_entry_errors(dummy_request):
    """Test detail view errors on non existant entry."""
    from learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = '1000'
    result = detail_view(dummy_request)
    assert result.status_code == 404


def test_create_view_returns_empty_list(dummy_request):
    """Test that create view returns an empty list."""
    from learning_journal.views.default import create_view
    assert create_view(dummy_request) == {}


def test_create_new_posts_adds_to_db(dummy_request):
    """Test that creating a posts adds a new post."""
    from learning_journal.views.default import create_view
    count = dummy_request.dbsession.query(Entry).count()
    dummy_request.method = 'POST'
    dummy_request.POST['title'] = 'test title'
    dummy_request.POST['category'] = 'test category'
    dummy_request.POST['tags'] = 'test tags'
    dummy_request.POST['body'] = 'test body'

    create_view(dummy_request)
    new_count = dummy_request.dbsession.query(Entry).count()
    assert new_count == count + 1


def test_edit_view_displays_post(dummy_request, add_posts):
    """Test edit view displays post that is passed through url."""
    from learning_journal.views.default import edit_view
    dummy_request.matchdict['id'] = '11'
    result = edit_view(dummy_request)
    entry = dummy_request.dbsession.query(Entry).get(11)
    assert result['entry'] == entry


def test_edit_old_post_updates_post(dummy_request, add_posts):
    """Test that creating a posts adds a new post."""
    from learning_journal.views.default import edit_view

    query = dummy_request.dbsession.query(Entry)

    dummy_request.method = 'POST'
    dummy_request.matchdict['id'] = '17'
    dummy_request.POST["title"] = 'test title'
    dummy_request.POST['category'] = 'test category'
    dummy_request.POST['tags'] = 'test tags'
    dummy_request.POST['body'] = 'test body'
    # import pdb; pdb.set_trace()
    edit_view(dummy_request)

    this_entry = query.get(17)
    assert this_entry['title'] == 'test title'
# Functional Tests


@pytest.fixture(scope="session")
def testapp(request):
    """Create an instance of webtests TestApp for testing routes."""
    from webtest import TestApp

    def main(global_config, **settings):
        """Return a Pyramid WSGI application."""
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('learning_journal.models')
        config.include('learning_journal.routes')
        config.include('learning_journal.security')
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

    def tearDown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(tearDown)

    return testapp


@pytest.fixture
def fill_the_db(testapp):
    """Fill the db with test data."""
    session_factory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        for entry in TEST_ENTRIES:
            post = Entry(title=entry['title'], body=entry['body'], category=entry['category'], creation_date=entry['creation_date'], tags=entry['tags'])
            dbsession.add(post)
    return dbsession


def test_layout_root(testapp):
    """Test that the contents of the root page contains <article>."""
    response = testapp.get('/', status=200)
    html = response.html
    assert 'Marc Fieser' in html.find("footer").text


def test_non_authenticated_user_cannot_access_create_view(testapp):
    """Test that accessing create new post is forbidden without auth."""
    response = testapp.get('/journal/new-entry', status=403)
    assert response.status_code == 403


# def test_user_can_log_in(set_auth_credentials, testapp):
#     """Test that a user can log in with correct credentials."""
#     testapp.post("/login", params={
#         "username": "testme",
#         "password": "foobar"
#     })
#     assert "auth_tkt" in testapp.cookie

# def test_create_view_contains_a_form(set_auth_credentials, testapp):
#     """Test that create view contains a form."""
#     response = testapp.get('/journal/new-entry', status=200)
#     html = response.html
#     assert len(html.find_all("form")) == 1


# def test_about_me_contains_info(testapp):
#     """Test that the about me page has content."""
#     response = testapp.get('/about')
#     html = response.html
#     assert 'About Me' in html.find('h1').text


# def test_create_view_redirects(set_auth_credentials, testapp):
#     """Test that a create view redirects."""
#     post_params = {'title': 'Test', 'body': 'body', 'category': 'testing', 'tags': ''}
#     response = testapp.post('/journal/new-entry', post_params, status=302)
#     assert response.status == '302 Found'


# def test_create_view_posts_new_form(set_auth_credentials, testapp):
#     """Test that a create view redirects."""
#     post_params = {'title': 'TestPOST', 'body': 'body', 'category': 'testing', 'tags': ''}
#     response = testapp.post('/journal/new-entry', post_params, status=302)
#     follow_response = response.follow()
#     assert 'TestPOST' in follow_response.html.find_all("article")[0].text


# def test_root_contents(testapp):
#     """Test that there are no entries on the page."""
#     fill_the_db(testapp)
#     response = testapp.get('/', status=200)
#     html = response.html
#     assert len(html.findAll("article")) == 5


# def test_detail_view_shows_correct_entry(testapp):
#     """Test that detail view shows the correct entry."""
#     fill_the_db(testapp)
#     response = testapp.get('/journal/2', status=200)
#     html = response.html
#     assert 'Testing Models 2' in html.text


# def test_category_view_display_correct_amount(testapp):
#     """Test that category view displays all of specific category."""
#     fill_the_db(testapp)
#     response = testapp.get('/journal/category/testing1', status=200)
#     html = response.html
#     assert len(html.findAll('article')) == 2
