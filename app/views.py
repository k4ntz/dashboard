from flask import render_template
from app import app
from getp import format_smis


@app.route('/')
def index():
    formated_dict, color_list = format_smis()
    res = render_template('template.html', formated_dict=formated_dict, color_list=color_list)
    return res
