# FortiDragon/admin_auth.py
from functools import wraps
from flask import g, abort

def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        user = getattr(g, 'user', None)
        if not user or user.get('role') != 'admin':
            abort(403)  # Forbidden
        return view(**kwargs)
    return wrapped_view