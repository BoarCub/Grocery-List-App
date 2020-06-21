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

SERVER_PATH = 'http://www.groceryreader.com/GL2020/images/'
# SERVER_PATH = 'http://www.dlearninglab.com/GL2020/'
UPLOAD_FOLDER = '/var/www/GL2020/images'
ALLOWED_EXTENSIONS = ['bmp', 'pdf', 'png', 'jpeg', 'TIFF']

DIETARY_TYPES = {'LOW-CARBOHYDRATE': 'Food low inCARBOHYDRATE',
                 'LOW-FAT/SUGAR': 'Food low in fat and sugar',
                 'HIGH-VITAMIN': 'Food high in vitamin',
                 'HIGH-PROTEIN': 'Food high in protein. Especially for people who are working out.'
                                 'HIGH-'
                 }


# SAMPLE API RETURN FOR LABELS
# {"Calories":"230","TotalFat":"8g","SaturatedFat":"1g","TransFat":"0g",
# "Cholesterol":"Omg","Sodium":"160mg","TotalCarbohydrate":"37g","DietaryFiber":"4g","Sugar":"1g","Protein":"3g"}

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

    # SAMPLE API RETURN FOR LABELS
    # {"Calories":"230","TotalFat":"8g","SaturatedFat":"1g","TransFat":"0g",
    # "Cholesterol":"Omg","Sodium":"160mg","TotalCarbohydrate":"37g","DietaryFiber":"4g","Sugar":"1g","Protein":"3g"}


@app.route('/report', methods=['GET', 'POST'])
@login_required
def report(title, json_data):
    return render_template('report.html', name=title, cal=json_data['Calories'], totalfat=json_data['TotalFat'],
                           sfat=json_data['SaturatedFat'], tfat=json_data['TransFat'], chole=json_data['Cholesterol'],
                           sodium=json_data['Sodium'], totalcarbo=json_data['TotalCarbohydrate'],
                           dfiber=json_data['DietaryFiber'], sugar=json_data['Sugar'], protein=json_data['Protein'])


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
        # Images for read only
        os.chmod(save_path, 0o444)
        # Call the first API to gain headline
        title = json_safe_get(call_api(API + SERVER_PATH + filename), 'title')
        if not title:
            return render_template('main.html', error_msg='Error fetching headline')
        # Call the second API to gain detailed information
        json_data = call_api(API2 + SERVER_PATH + filename)
        if len(json_data) != 10:
            return render_template('main.html', error_msg='Error fetching detailed information')
        for key in json_data.keys:
            if json_data[key] == '':
                json_data[key] = 'No data fetched'
        return report(title, json_data)
    else:
        return render_template('main.html', error_msg='File is blank or the file format is not allowed')


def call_api(path):
    try:
        return json.loads(req.get(url=path).text)
    except:
        return None


# Call this function if the json data is not ensured filled with data and may cause KeyError if fetched directly
def json_safe_get(json, key):
    if not json or key not in json:
        return None
    try:
        return json[key]
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
