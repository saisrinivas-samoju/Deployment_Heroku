from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):
    sepal_length= StringField('What is the Sepal Length? in cm: ', validators = [DataRequired()])
    sepal_width= StringField('What is the Sepal Width? in cm: ', validators = [DataRequired()])
    petal_length= StringField('What is the Petal Length? in cm: ', validators = [DataRequired()])
    petal_width= StringField('What is the Petal Width? in cm: ', validators = [DataRequired()])
    submit = SubmitField('Predict')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods = ['GET','POST'])
def predict():
    form = InfoForm()
    show = False
    if form.validate_on_submit():
        show = True
        session['sepal_length'] = float(form.sepal_length.data)
        session['sepal_width'] = float(form.sepal_width.data)
        session['petal_length'] = float(form.petal_length.data)
        session['petal_width'] = float(form.petal_width.data)
        flash(f"The features belong to {model.predict([[session['sepal_length'], session['sepal_width'],session['petal_length'],session['petal_width'] ]])[0].upper()}")
        return redirect(url_for('predict'))
    form.sepal_length.data = ''
    form.sepal_width.data = ''
    form.petal_length.data = ''
    form.petal_width.data = ''
    return render_template('predict.html', form=form, model=model, show=show)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
