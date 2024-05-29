from flask import Flask, render_template, request
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,FileField
from wtforms import DecimalField, RadioField, SelectField,TextAreaField,SubmitField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask import url_for

app =Flask(__name__) #static_folder="photos", static_url_path="/photos" # if we have photos folder insted of static, we have to set static config properties
                                                                        # app have by defalut static folder configuration.
app.debug=True
app.config['SECRET_KEY']='0123456789'
app.config['UPLOAD_PATH']='/Users/mac/Documents/Flask/flask_wtf/flask_wtf/static'

class MyForm(FlaskForm):
    name=StringField('Name',validators=[InputRequired()])
    password=PasswordField('Password', validators=[InputRequired()])
    remember_me=BooleanField('Remember me')
    salary=DecimalField('Salary', validators=[InputRequired()])
    gender=RadioField('Gender',choices=[('male','Male'),('female','Female')])
    country=SelectField('Country', choices=[('IN','India'),('US','United States'),('UK','United Kingdom')])
    message= TextAreaField('Message',validators=[InputRequired()])
    photo=FileField('Photo')

@app.route('/',methods=['GET','POST'])
def index():
    form=MyForm()
    if form.validate_on_submit():
        name=form.name.data
        password=form.password.data
        remember_me=form.remember_me.data
        salary=form.salary.data
        gender=form.gender.data
        country=form.country.data
        message=form.message.data
        f=form.photo.data
        photo=secure_filename(f.filename)
        f.save(os.path.join(app.config["UPLOAD_PATH"],photo))
        
        return f'Name: {name}<br>Password:{generate_password_hash(password)}<br>Remember me:{remember_me}<br>Salary:{salary}\
    <br>Gender:{gender}<br>Country:{country}<br>Message:{message}<br>Photo:{photo} <br><img style="width:450px" src="http://127.0.0.1:5001/static/{photo}" alt="{photo}">' #<img src="/photos/{photo}" alt="{photo}">'
    return render_template('index.html',form=form)

class LoginForm(FlaskForm):
    username=StringField('Username',validators=[InputRequired('Username Required!'),
                                                Length(min=5, max=25, message='Username must be in 5 to 25 characters')])
    password=PasswordField('Password',validators=[InputRequired('Password required')])
    submit=SubmitField('Submit')

@app.route('/Signup', methods=['GET','POST'])
def form():
    form=LoginForm()
    if form.validate_on_submit():
        return '<h1>Hi {}!!. Your form is submitted successfully!!'.format(form.username.data)
    return render_template('Signup.html', form=form)

if __name__=='__main__':
    app.run(host='127.0.0.1',port=5001)