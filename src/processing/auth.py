from functools import wraps

from flask import redirect, url_for, session


def requires_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check the session
        if session.get('user') is None:
            return redirect(url_for('website.login'))
        return f(session['user'], *args, **kwargs)
    return decorated_function
