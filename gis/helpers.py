from flask import session, redirect
from functools import wraps


# Functions to convert different types of coordinates to decimal degrees
def coords_calc(dd, mm, ss):
    d, m, s = float(dd), float(mm), float(ss)
    coord = d + (m / 60) + (s / 3600)
    return round(coord, 6)


def coords_calc_new(dd, mm_mmmm):
    d, m = float(dd), float(mm_mmmm)
    coord = d + (m / 60)
    return round(coord, 6)


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    function is taken from the cs50 course, PS Finance
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
