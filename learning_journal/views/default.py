from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError

from ..models import Entry
import datetime


@view_config(route_name='list', renderer='templates/list.jinja2')
def list_view(request):
    """List_view view to supply entries before database."""
    try:
        entries = request.dbsession.query(Entry).order_by(Entry.creation_date.desc()).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {"entries": entries}


@view_config(route_name="detail", renderer="../templates/detail.jinja2")
def detail_view(request):
    """View for individual post."""
    query = request.dbsession.query(Entry)
    the_entry = query.filter(Entry.id == request.matchdict['id']).first()
    return {"entry": the_entry}


@view_config(route_name='create', renderer='../templates/create.jinja2')
def create_view(request):
    """View for creating a new post."""
    if request.method == "POST":
        new_title = request.POST["title"]
        new_body = request.POST["body"]
        new_date = datetime.datetime.now().date()
        new_category = request.POST["category"]
        new_tags = request.POST["tags"]
        new_entry = Entry(title=new_title, body=new_body, creation_date=new_date, category=new_category, tags=new_tags)
        
        request.dbsession.add(new_entry)

        return HTTPFound(location='/')
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
