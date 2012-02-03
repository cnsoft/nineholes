# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_
from nineholes import model
from repoze.what import predicates
from nineholes.controllers.secure import SecureController
from nineholes.model import Challenge, Entry, DBSession, metadata

from nineholes.lib.base import BaseController
from nineholes.controllers.error import ErrorController

from urllib2 import urlopen
import transaction

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the nineholes application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """

    error = ErrorController()

    @expose('nineholes.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('nineholes.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('nineholes.templates.import_vimgolf')
    def import_vimgolf(self, challenge_id=None):
        """Import a challenge from vimgolf website"""
        challenge_file = urlopen("http://vimgolf.com/challenges/%s.yaml" % challenge_id)
        if challenge_file:
            yaml_conf = load(challenge_file, Loader=Loader)
            file_in = yaml_conf['in']['data'] 
            file_out = yaml_conf['out']['data']
            file_vimrc = yaml_conf['vimrc']

        if DBSession.query(model.Challenge).filter(model.Challenge.id==challenge_id).count():
            # Dont import file, redirect instead
            redirect("/?challenge=%s" % challenge_id)
        
        new_challenge = model.Challenge()
        new_challenge.title = "VimGolf Challenge: %s" % challenge_id
        new_challenge.start_file = file_in
        new_challenge.final_file = file_out
        new_challenge.vimrc = file_vimrc
        new_challenge.challenge_key = challenge_id
        DBSession.add(new_challenge)
        DBSession.flush()

        transaction.commit()
        redirect("/?challenge=%s" % challenge_id)

        return dict(page="import_vimgolf", 
            file_in=file_in, 
            file_out=file_out)

    @expose('nineholes.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login',
                params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
