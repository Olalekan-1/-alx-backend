#!/usr/bin/env python3

""" Set up python flask application """

from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


class Config:
    """ defines the configuration for Babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@app.route('/')
def index():
    """ returns the rendered template"""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(debug=True)
