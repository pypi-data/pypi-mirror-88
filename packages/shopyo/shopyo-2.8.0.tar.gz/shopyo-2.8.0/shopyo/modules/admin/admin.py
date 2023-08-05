from functools import wraps

from flask import flash
from flask import redirect
from flask import url_for

from flask_login import current_user

from shopyoapi.init import login_manager

from modules.admin.models import User

login_manager.login_view = "login.login"
login_manager.login_message = "Please login for access"


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_admin is True:
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page.")
            return redirect(url_for("control_panel.index"))

    return wrap
