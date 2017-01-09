"""Default views for learning journal web app."""

from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.security import remember, forget
from learning_journal.security import check_credentials

from ..models import Entry
import datetime

# ==================== Views with only GET ====================


@view_config(route_name='list', renderer='templates/list.jinja2')
def list_view(request):
    """List_view view to supply entries before database."""
    count = 0
    entries = request.dbsession.query(Entry).order_by(Entry.creation_date.desc()).all()
    if len(entries) > 0:
        count = request.dbsession.query(Entry).order_by(Entry.id.desc()).first().id
    if request.method == "POST":
        new_title = request.POST["title"]
        new_body = request.POST["body"]
        new_date = datetime.datetime.now().date()
        new_category = request.POST["category"].title().replace(" ", "")
        new_tags = request.POST["tags"]
        new_entry = Entry(title=new_title, body=new_body, creation_date=new_date, category=new_category, tags=new_tags)

        request.dbsession.add(new_entry)
    return {"entries": entries, "count": count}


@view_config(route_name="detail", renderer="../templates/detail.jinja2")
def detail_view(request):
    """View for individual post."""
    query = request.dbsession.query(Entry)
    the_entry = query.filter(Entry.id == request.matchdict['id']).first()
    if not the_entry:
        return Response("Not Found", content_type='text/plain', status=404)
    return {"entry": the_entry}


@view_config(route_name="category", renderer="../templates/category.jinja2")
def category_view(request):
    """View for post of different categories."""
    query = request.dbsession.query(Entry)
    entries = query.filter(Entry.category == request.matchdict['category']).order_by(Entry.creation_date.desc()).all()
    return {"entries": entries}


@view_config(route_name="about", renderer="../templates/about.jinja2")
def about_view(request):
    """View for about me."""
    return {}


# ========================= Views that update DB =================


@view_config(route_name='create', renderer='../templates/create.jinja2', permission='create')
def create_view(request):
    """View for creating a new post."""
    if request.method == "POST":
        new_title = request.POST["title"]
        new_body = request.POST["body"]
        new_date = datetime.datetime.now().date()
        new_category = request.POST["category"].title().replace(" ", "")
        new_tags = request.POST["tags"]
        new_entry = Entry(title=new_title, body=new_body, creation_date=new_date, category=new_category, tags=new_tags)

        request.dbsession.add(new_entry)

        return HTTPFound(request.route_url("list"))
    return {}


@view_config(route_name='edit', renderer='../templates/edit.jinja2', permission='edit')
def edit_view(request):
    """View for creating a new post."""
    query = request.dbsession.query(Entry)
    the_entry = query.filter(Entry.id == request.matchdict['id']).first()
    if request.method == "POST":
        the_entry.title = request.POST["title"]
        the_entry.body = request.POST["body"]
        the_entry.category = request.POST["category"].title().replace(" ", "")
        the_entry.tags = request.POST["tags"]

        # request.dbsession.flush(the_entry)

        return HTTPFound(request.route_url("list"))
    return {"entry": the_entry}


@view_config(route_name='delete', permission='delete')
def delete_view(request):
    """To delete entries from journal."""
    # import pdb; pdb.set_trace()
    entry = request.dbsession.query(Entry).get(request.matchdict['id'])
    request.dbsession.delete(entry)
    return HTTPFound(request.route_url('list'))


# =================== Views for login/logout ==================


@view_config(route_name='login', renderer='../templates/login.jinja2', permission=NO_PERMISSION_REQUIRED, require_csrf=False)
def login_view(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password):
            auth_head = remember(request, username)
            return HTTPFound(
                request.route_url("list"),
                headers=auth_head
            )
    return {}


@view_config(route_name="logout")
def logout_view(request):
    auth_head = forget(request)
    return HTTPFound(request.route_url('list'), headers=auth_head)

# ====================== HTTP Pages =======================


@forbidden_view_config(renderer="../templates/forbidden.jinja2")
def not_allowed_view(request):
    """Some special stuff for the forbidden view."""
    request.response.status = 403
    return {}

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
