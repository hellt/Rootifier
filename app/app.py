from flask import Flask, render_template, redirect, url_for
import os
import config


root_folder_path = os.path.dirname(os.path.abspath(__file__))

# get env_settings list
env_settings = config.EnvironmentSettings(root_folder_path)

# initialize Flask app
app = Flask(__name__)


from sros_rootifier.sros_rootifier import sros_rootifier_bp
app.register_blueprint(sros_rootifier_bp)

@app.route('/')
def index():
    return redirect('/sros_rootifier')

@app.route('/about')
def about():
    return render_template('index.html')

if __name__ == '__main__':
    # configure Flask app from a class, stored in PLAZA_SETTINGS variable
    app.config.from_object(env_settings['PLAZA_SETTINGS'])
    # if we are in Prod, use HOST and PORT specified
    try:
        app.run(host=str(env_settings['HOST']), port=80)
    except config.ConfigurationError:
        app.run()
