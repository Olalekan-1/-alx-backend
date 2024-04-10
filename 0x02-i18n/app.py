#!/usr/bin/env python3

""" Set up python flask application """

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz


app = Flask(__name__)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale():

    """ Get the locale language """

    if 'locale' in request.args:
        requested_locale = request.args.get('locale')
        if requested_locale in app.config['LANGUAGES']:
            return requested_locale

    if hasattr(g, 'user') and g.user and 'locale' in g.user:
        user_locale = g.user['locale']
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    accept_languages = request.accept_languages
    best_match = accept_languages.best_match(app.config['LANGUAGES'])
    if best_match:
        return best_match

    return app.config['BABEL_DEFAULT_LOCALE']


def get_timezone():
    """ get and set time zone """
    if 'timezone' in request.args:
        requested_timezone = request.args.get('timezone')
        try:
            pytz.timezone(requested_timezone)
            return requested_timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    if hasattr(g, 'user') and g.user and 'timezone' in g.user:
        user_timezone = g.user['timezone']
        try:
            pytz.timezone(user_timezone)
            return user_timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


def get_user(user_id):
    """ Gets user id """
    return users.get(user_id)


@app.before_request
def before_request():
    """ display before request """
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None


@app.route('/')
def index():
    """ index html """
    if g.user:
        welcome_message = _("You are logged in as %(username)s.") \
            % {'username': g.user['name']}
    else:
        welcome_message = _("You are not logged in.")
    return render_template('7-index.html', welcome_message=welcome_message)


if __name__ == '__main__':
    app.run(debug=True)
