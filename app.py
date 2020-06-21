import json
import random
import os
import requests as req
from flask import Flask, request, flash, render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# The . is a shortcut that tells it search in current package before rest of the PYTHONPATH
# from .auth import login_required

app = Flask(__name__)

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
API = 'https://groceryreaderv6-1.azurewebsites.net/api/ReadOCRLines?url='
API2 = 'https://nutritionalreaderv1.azurewebsites.net/api/NutritionLines?url='

# SERVER_PATH = 'http://groceryreader.com/GL2020/'
SERVER_PATH = 'http://www.dlearninglab.com/GL2020/'
UPLOAD_FOLDER = '/var/www/GL2020/images'
ALLOWED_EXTENSIONS = ['bmp', 'pdf', 'png', 'jpeg', 'TIFF']


@app.route('/main', methods=['GET'])
@login_required
def main_page():
    return render_template('main.html')


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    if current_user.is_authenticated:
        # If user is logged in, just redirected to user main page.
        return redirect(url_for('main_page'))
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/api/upload_img', methods=['POST'])
@login_required
def upload_img():
    if 'file' not in request.files:
        return render_template('main.html', error_msg='No file selected')
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(str(random.random()) + file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
        os.chmod(save_path, 0o444)
        # Call the first API to gain headline
        title = call_api(API + SERVER_PATH + 'images/' + filename)
        if not title or title['status'] == 'Running':
            return render_template('main.html', error_msg='Error fetching headline')
        # Call the second API to gain detailed information
        json_data = call_api(API2 + SERVER_PATH + 'images/' + filename)
        if not json_data or json_data['status'] == 'Running':
            return render_template('main.html', error_msg='Error fetching detailed information')

        return render_template('main.html', base_msg=json_data)
    else:
        return render_template('main.html', error_msg='File is blank or the file format is not allowed')


def call_api(path):
    try:
        return json.loads(req.get(url=path).text)
    except:
        return None


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app():
    app.config['SECRET_KEY'] = 'iamthesecretekeytodatabase'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users/users.db'

    db.init_app(app)

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    app_blueprint = Blueprint('app', __name__)
    app.register_blueprint(app_blueprint)
    return app


"""
Call this function when you want to test your program on a development server
Rename __init__ to wsgi file if you want to deploy on production server
"""


def run_app():
    app.config['SECRET_KEY'] = 'iamthesecretekeytodatabase'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users/users.db'

    db.init_app(app)

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # print('User ID:', user_id)
        # since the user_id is just the primary key of our user table, use it in the query for the user
        from user import User
        return User.query.get(int(user_id))
    app.run()


if __name__ == '__main__':
    run_app()
