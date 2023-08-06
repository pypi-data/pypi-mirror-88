# from django.utils.thread_support import currentThread
from threading import currentThread

from django.utils.deprecation import MiddlewareMixin
from django_utils.mock_request import MockRequest

_requests = {}

def get_request():
    return _requests[currentThread()]

def get_thread_user():
    try:
        return get_request().user
    except:
        return None

def set_request(request):
    _requests[currentThread()] = request

def delete_request():
    del _requests[currentThread()]

class GlobalRequestMiddleware(object):
    def process_request(self, request):
        _requests[currentThread()] = request

class GlobalRequestMiddleware(MiddlewareMixin):
    # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        set_request(request)
        response = self.get_response(request)
        delete_request()
        return response

def with_global_user(func):
    def wrapped_func(*args, _user=None, **kwargs):
        if len(args) > 0:
            if hasattr(args[0], 'user'):
                user = args[0].user
        if 'user'in kwargs:
            user = kwargs['user']
        if _user:
            user = _user
        assert user is not None, "User can't be none"
        set_request(MockRequest(user))
        res = func(*args, **kwargs)
        delete_request()
        return res
    return wrapped_func