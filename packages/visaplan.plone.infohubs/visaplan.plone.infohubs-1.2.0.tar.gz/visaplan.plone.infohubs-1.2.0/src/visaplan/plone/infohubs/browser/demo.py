# -*- coding: utf-8 -*-
from traceback import format_exc

# Zope:
from Products.Five import BrowserView
from zope.interface import implements

# visaplan:
from .. import make_hubs
from visaplan.tools.lands0 import list_of_strings
from visaplan.tools.debug import pp

from .interfaces import IInfohubsDemo


class Browser(BrowserView):
    """
    Feed @@infohubs-demo; (gf)
    templates/infohubs-demo.pt
    """

    implements(IInfohubsDemo)

    def data(self):
        context = self.context
        request = self.request
        form = request.form

        # sorted list of implemented keys:
        key_tuples = self.infokeys()
        # from pdb import set_trace; set_trace()
        DESCRIPTION = dict(key_tuples)

        hub_rows = []
        info_rows = []
        overview_rows = []
        keys = list_of_strings(form.get('keys'))
        hub, info = make_hubs(context, ordered=True)
        DONE = set()
        ERRORS = {}
        if keys:
            for key in keys:
                if key in DONE:
                    continue
                try:
                    val = info[key]
                except Exception as e:
                    ERRORS[key] = format_exc()
                else:
                    DONE.add(key)

            # now get the info keys in the order they have been created:
            for key, val in info.items():
                info_rows.append({
                    'key': key,
                    'ok': True,
                    'value': val,
                    'type': type(val),
                    'implicit': key not in keys,
                    'description': DESCRIPTION.get(key),
                    })

            # did we get errors?
            for key in keys:
                if key in DONE:
                    continue
                info_rows.append({
                    'key': key,
                    'ok': False,
                    'implicit': key not in keys,
                    'error': ERRORS.get(key),
                    'description': DESCRIPTION.get(key),
                    })
                DONE.add(key)

            # now get the hub keys in the order they have been created:
            for key, val in hub.items():
                hub_rows.append({
                    'key': key,
                    'value': val,
                    })

        # the full list of documented info keys,
        # with values merged in:
        for key, descr in key_tuples:
            row = {
                'key': key,
                'description': descr,
                }
            if key in info:
                spice = {
                    'ok': True,
                    'done': True,
                    'value': info[key],
                    }
            elif key in ERRORS:
                spice = {
                    'ok': False,
                    'done': True,
                    }
            else:
                spice = {
                    'ok': None,
                    'done': False,
                    }
            row.update(spice)
            overview_rows.append(row)

        res = {
            'keys': ' '.join(keys),
            'info': info_rows,
            'hub': hub_rows,
            'available': overview_rows,
            }
        pp(res=res)
        # set_trace()
        return res

    def infokeys(self):
        raw = [
            ('portal', 1, 'portal_object',
                          'The (Plone) portal object'),
            ('portal', 2, 'portal_id',
                          'The ID of the portal object'),
            ('portal', 3, 'portal_url',
                          'absolute_url() of the (Plone) portal object'),
            ('portal', 4, 'portal_and_site_objects',
                          'get_portal_and_site'),

# user:
            ('user', 1, 'logged_in',
                          'Is the current user logged in?'),
            ('user', 2, 'user_object',
                          'the authenticated user, or None'),
            ('user', 3, 'user_id',
                          'User ID (or None?)'),
            ('user', 4, 'user_email',
                          'User E-Mail address (from acl_users?)'),

# function proxies
            ('function proxies', 2, 'is_member_of',
                          "is info['user_id'] a member of ...?"),

# context
            ('context', 1, 'portal_type',
                          'portal_type of context'),
            ('context', 2, 'context_url',
                          'url of context'),
            ('context', 3, 'context_title',
                          'title of context'),
            ('context', 10, 'context_owner',
                          'owner of context'),
            ('context', 4, 'context_as_brain',
                          'brain of context'),
            ('context', 2, 'my_uid',
                          "UUID of context ('root' for site root)"),
            ('context', 2, 'has_uid',
                          'does the context have a UUID?'
                          ' (currently by .UID() method call)'),
            ('context', 21, 'is_mine',
                          'context object is owned by the active user'),
# request
            ('request', 2, 'request',
                          'the request object'),
            ('request', 2, 'request_var',
                          'the request.form dictionary'),
            ('request', 2, 'response',
                          'the response object'),
            ('request', 2, 'session',
                          'a proxy to read and write session variables'),
# language
            ('language', 1, 'current_lang',
                          '2-letter code of the current display language'),
            ]
        return [tup[2:] for tup in sorted(raw)]
