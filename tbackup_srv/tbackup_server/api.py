# -*- coding: utf-8 -*-

import simplejson as json

from django.http import HttpResponse

def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)

        if isinstance(resp, HttpResponse):
            return resp

        return HttpResponse(json.dumps(resp), mimetype="application/json")

    return wrap