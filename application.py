

from flask import Flask, request, redirect, url_for, flash, \
    render_template, send_from_directory, jsonify, request
from werkzeug.utils import secure_filename
from astropy import log
from flask_bootstrap import Bootstrap

from aws_controller.upload_download_s3 import upload_to_s3

from app import InputForm, LoginForm

from app import db
from app.models import Data
from app.forms import EnterDBInfo, RetrieveDBInfo

from flask.ext.sqlalchemy import SQLAlchemy



UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config.AWSConfig')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

key = app.config['AWS_KEY']
secret = app.config['AWS_SECRET']


@app.route("/")
def default():
    # display welcome page
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = InputForm()
    form.filename(multiple="")
    if request.method == "POST":
        if form.validate_on_submit():
            return redirect('/')
        else:
            return render_template('submit.html', form=form)
    return render_template('submit.html', form=form)


#@app.route('/upload', methods=['POST'])
#def upload(timestamp):
#    if request.method == 'POST':
#        data_file = request.files('file')
#        file_name = secure_filename(data_file.filename)
#        upload_to_s3(timestamp, file_name, create_bucket=True,
#                     aws_access={"aws_access_key_id": key,
#                                 "aws_secret_access_key": secret})

#        return jsonify(name=file_name)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form1 = EnterDBInfo(request.form) 
    
    if request.method == 'POST' and form1.validate():
        user_name=form1.username.data
        query_test=Data.query.filter_by(nickname=user_name.encode('ascii','ignore')).first()
        if query_test!=None:
            string_response='You already have an account. Please sign in.'
            return render_template('thanks2.html', output=string_response) 
        else:
            data_entered = Data(nickname=form1.username.data,password=form1.passwd.data,inst=form1.institute.data,emailaddress=form1.email_ad.data)
            try:     
                db.session.add(data_entered)
                db.session.commit()        
                db.session.close()
            except:
                db.session.rollback()
            return render_template('thanks.html', nickname=form1.username.data,password=form1.passwd.data)
        
    return render_template('login.html', form=form1)

@app.route("/login2", methods=['GET', 'POST'])
def login2():
    form2 = RetrieveDBInfo(request.form) 
        
    if request.method == 'POST' and form2.validate():
        user_return = form2.username_ret.data
        passwd_return = form2.passwd_ret.data
        user_query=Data.query_by_name(user_return.encode('ascii','ignore'),passwd_return.encode('ascii','ignore'))
        if user_query[1]=='no_password':
            string_response='The password entered for username: '+user_query[0]+' is incorrect. Please try again.'
            return render_template('thanks2.html', output=string_response) 
        elif user_query=='no_user':
            string_response='The username: '+user_query[0]+' does not exist in the database. Please sign up.'
            return render_template('thanks2.html', output=string_response) 
        else:
            return redirect(url_for('submit'))
        db.session.close()

    return render_template('login2.html', form=form2)

if __name__ == '__main__':
    log.setLevel(10)
    app.run(debug=True)
