from flask import render_template, flash, redirect
from app import app
from .forms import RsForm
from .logic import *

@app.route('/', methods=['GET', 'POST'])
@app.route('/rs', methods=['GET', 'POST'])
def rs(): 
    form = RsForm()
    #to set a default value
    #form.conversion_query.data = ''
    if form.validate_on_submit(): 
        result = calculate_missing(form.conversion_query.data)
        #flash('Query requested: ' + form.conversion_query.data + ', result: ' + str(result))
        # return redirect('/rs')
        return render_template('calculator.html', title='Exercise Stats', form=form, result=result)

    return render_template('calculator.html', title='Exercise Stats', form=form)
