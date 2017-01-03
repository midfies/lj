"""Security.py for learning_journal."""
import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated, Everyone
from passlib.apps import custom_app_context as pwd_context


class NewRoot(object):
    """Class for newroot."""

    def __init__(self, request):
        """Init newroot."""
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'create'),
        (Allow, Authenticated, 'edit'),
    ]


def check_credentials(username, password):
    """Raturn True if valid username and password, else false."""
    if username and password:
        # proceed to check credentials
        if username == os.environ["AUTH_USERNAME"]:
            return pwd_context.verify(password, os.environ["AUTH_PASSWORD"])
    return False


def includeme(config):
    """security-related configuration."""
    auth_secret = os.environ.get('AUTH_SECRET', 'itsaseekrit')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    # config.set_default_permission('view')
    config.set_root_factory(NewRoot)
