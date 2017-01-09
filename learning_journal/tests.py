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
def test_to_json():
    """Tets the to_json method returns a dict."""
    from learning_journal.models import Entry
    new_entry = Entry(title='new_title', body='new_body', creation_date='new_date', category='new_category', tags='new_tags')
    assert isinstance(new_entry.to_json(), dict)


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
    dummy_request.matchdict['id'] = '12'
    result = edit_view(dummy_request)
    entry = dummy_request.dbsession.query(Entry).get(12)
    assert result['entry'] == entry


def test_edit_old_post_updates_post(dummy_request, add_posts):
    """Test that creating a posts adds a new post."""
    from learning_journal.views.default import edit_view

    query = dummy_request.dbsession.query(Entry)

    dummy_request.method = 'POST'
    dummy_request.matchdict['id'] = '18'
    dummy_request.POST["title"] = 'test title'
    dummy_request.POST['category'] = 'test category'
    dummy_request.POST['tags'] = 'test tags'
    dummy_request.POST['body'] = 'test body'
    edit_view(dummy_request)
    this_entry = query.get(18)
    assert this_entry.title == 'test title'


def test_category_view_returns_with_correct_category(dummy_request, add_posts):
    """Test that category review returns entry with proper categoty."""
    from learning_journal.views.default import category_view
    dummy_request.matchdict['category'] = 'testing1'
    result = category_view(dummy_request)
    assert result['entries'][0].category == 'testing1'


def test_about_view_returns_empty_dict(dummy_request):
    """Test about view returns empty dict."""
    from learning_journal.views.default import about_view
    assert about_view(dummy_request) == {}


def test_login_view_returns_empty_dict(dummy_request):
    """Test login view returns empty dict."""
    from learning_journal.views.default import login_view
    assert login_view(dummy_request) == {}


def test_check_credentials_passes_with_good_creds(set_auth_credentials):
    """Test that check credentials works with valid creds."""
    from learning_journal.security import check_credentials
    assert check_credentials("testme", "foobar")


def test_check_credentials_fails_with_bad_password(set_auth_credentials):
    """Test that check credential fails on bad password."""
    from learning_journal.security import check_credentials
    assert not check_credentials("testme", "bad pass")


def test_check_credentials_fails_with_bad_username(set_auth_credentials):
    """Test that check credential fails on bad username."""
    from learning_journal.security import check_credentials
    assert not check_credentials("bad username", "foobar")


def test_check_credentials_fails_empty_creds(set_auth_credentials):
    """Test that check credential fails with no credentials."""
    from learning_journal.security import check_credentials
    assert not check_credentials("", "")


def test_login_view_good_creds_gets_redirect(dummy_request, set_auth_credentials):
    """Test that logging in with cred redirects to home."""
    from learning_journal.views.default import login_view
    from pyramid.httpexceptions import HTTPFound
    dummy_request.method = "POST"
    dummy_request.POST["username"] = "testme"
    dummy_request.POST["password"] = "foobar"
    result = login_view(dummy_request)
    assert isinstance(result, HTTPFound)


def test_login_view_with_bad_creds_stays(dummy_request, set_auth_credentials):
    """Test that loggin in does nothing with bad credentials."""
    from learning_journal.views.default import login_view
    dummy_request.method = "POST"
    dummy_request.POST["username"] = "nameuser"
    dummy_request.POST["password"] = "wordpass"
    result = login_view(dummy_request)
    assert result == {}


def test_logout_returns_to_home(dummy_request):
    """Test that logout returns with httpfound to home."""
    from learning_journal.views.default import logout_view
    result = logout_view(dummy_request)
    assert result.status_code == 302


def test_delete_view_redirects(dummy_request, add_posts):
    """Test that delete view redirets back to the home page."""
    from learning_journal.views.default import delete_view
    dummy_request.matchdict['id'] = '27'
    result = delete_view(dummy_request)
    assert result.status_code == 302



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
    assert len(html.find_all('article')) == 0


def test_detail_view_returns_not_found_when_db_empty(testapp):
    """Test detail view returns not found when no entries."""
    response = testapp.get('/journal/1', status=404)
    assert response.status_code == 404


def test_non_authenticated_user_cannot_access_create_view(testapp):
    """Test that accessing create new post is forbidden without auth."""
    response = testapp.get('/journal/new-entry', status=403)
    assert response.status_code == 403


def test_non_authenticated_user_cannot_access_edit_view(testapp):
    """Test that accessing edit post is forbidden without auth."""
    response = testapp.get('/journal/1/edit-entry', status=403)
    assert response.status_code == 403


def test_category_view_contains_no_entries_with_empty_db(testapp):
    """Test that category view has no articles with empty db."""
    response = testapp.get('/journal/category/testing', status=200)
    html = response.html
    assert len(html.find_all('article')) == 0


def test_about_me_page_contains_about_me(testapp):
    """Test about me page contains about me content."""
    response = testapp.get('/about', status=200)
    html = response.html
    assert 'About Me' in html.find("title").text


def test_login_page_has_login_form(testapp):
    """Test about me page contains about me content."""
    response = testapp.get('/login', status=200)
    html = response.html
    assert 'Log In' in html.find("title").text
    assert len(html.find_all('form')) == 1

# ======================Let the data start=====================


def test_home_view_with_data_lists_all_articles(testapp, fill_the_db):
    """When there's data in the database, the home page has articles."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("article")) == 5


def test_detail_view_has_specific_article(testapp):
    """Test that a specific article is loaded in detail view."""
    response = testapp.get("/journal/1")
    assert len(response.html.find_all("article")) == 1
    assert "Testing Models 1" in response.text


def test_user_can_log_in(set_auth_credentials, testapp):
    """Test that a user can log in with correct credentials."""
    testapp.post("/login", params={
        "username": "testme",
        "password": "foobar"
    })
    assert "auth_tkt" in testapp.cookies


def test_create_view_contains_a_form(testapp):
    """Test that create view contains a form."""
    response = testapp.get('/journal/new-entry', status=200)
    html = response.html
    assert len(html.find_all("form")) == 1


def test_create_view_redirects_and_updates_db(testapp):
    """Test that a create view redirects."""
    response = testapp.get("/journal/new-entry")
    csrf_token = response.html.find(
        "input",
        {"name": "csrf_token"}).attrs["value"]

    post_params = {'csrf_token': csrf_token, 'title': 'TestPOST', 'body': 'body', 'category': 'testing', 'tags': ''}
    response = testapp.post('/journal/new-entry', post_params, status=302)
    assert response.status == '302 Found'
    follow_response = response.follow()
    assert 'TestPOST' in follow_response.html.find_all("article")[0].text


def test_edit_view_redirects_and_updates_db(testapp):
    """Test that a edit view redirects."""
    response = testapp.get("/journal/6/edit-entry")
    csrf_token = response.html.find(
        "input",
        {"name": "csrf_token"}).attrs["value"]

    post_params = {'csrf_token': csrf_token, 'title': 'TestPOST Edit', 'body': 'body', 'category': 'testing', 'tags': ''}
    response = testapp.post('/journal/6/edit-entry', post_params, status=302)
    assert response.status == '302 Found'
    follow_response = response.follow()
    assert 'TestPOST Edit' in follow_response.html.find_all("article")[0].text


def test_category_view_display_correct_amount(testapp):
    """Test that category view displays all of specific category."""
    response = testapp.get('/journal/category/testing1', status=200)
    html = response.html
    assert len(html.findAll('article')) == 2


def test_posting_from_home_adds_to_db(testapp):
    """Test that you can post from the home page."""
    response = testapp.get('/')
    assert len(response.html.find_all("article")) == 6
    csrf_token = response.html.find(
        "input",
        {"name": "csrf_token"}).attrs["value"]
    post_params = {'csrf_token': csrf_token, 'title': 'TestHomePost', 'body': 'body', 'category': 'testing', 'tags': ''}
    response = testapp.post('/', post_params)
    response = testapp.get('/')
    assert 'TestHomePost' in response.html.text


def test_logout_view_logs_out_user(testapp):
    """Test that logging out revokes the token."""
    testapp.get('/logout')
    assert "auth_tkt" not in testapp.cookies
