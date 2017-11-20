import os

from flask import Flask, redirect, render_template, url_for

import config
from sros_rootifier.sros_rootifier import sros_rootifier_bp

root_folder_path = os.path.dirname(os.path.abspath(__file__))

# get env_settings list
env_settings = config.EnvironmentSettings(root_folder_path)

# initialize Flask app
app = Flask(__name__)


app.register_blueprint(sros_rootifier_bp)


@app.route('/')
def index():
    return redirect('/sros_rootifier')


if __name__ == '__main__':
    # configure Flask app from a class, stored in PLAZA_SETTINGS variable
    app.config.from_object(env_settings['PLAZA_SETTINGS'])
    # if we are in Prod, use HOST and PORT specified
    try:
        app.run(host=str(env_settings['HOST']), port=80)
    except config.ConfigurationError:
        app.run()
