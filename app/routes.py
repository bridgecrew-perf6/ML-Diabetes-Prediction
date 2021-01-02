from flask import render_template, flash, Markup, request, current_app as app, jsonify
import numpy
from app import model
from app.forms import DiagnoseForm


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("home.html", title='Home')


@app.route("/diagnose", methods=['GET'])
def diagnose():
    form = DiagnoseForm()
    return render_template("diagnose.html",
                           form=form,
                           title='Diagnose')


@app.route('/diagnosis', methods=['POST'])
def diagnosis():
    form = DiagnoseForm()
    if form.validate_on_submit():
        gender = (form.gender.data == 'True') # Convert boolean to string
        polyuria = form.polyuria.data
        polydipsia = form.polydipsia.data
        sudden_wl = form.sudden_wl.data
        obesity = form.obesity.data
        features = [gender, polyuria, polydipsia, sudden_wl, obesity]
        prediction = 'Positive' if model.predict([features]) else 'Negative'  # Convert boolean to string
        accuracy = "{:.2f}".format(round((numpy.max(model.predict_proba([features])) / 1), 2))
        results = {'prediction': prediction,
                   'accuracy': accuracy}
        return results

    return jsonify(data=form.errors)


@app.route("/about")
def about():
    return render_template("about.html", title='About')