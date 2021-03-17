from flask import Blueprint, request, render_template, redirect, url_for, flash
from app import app 
import json
import os

main = Blueprint("main", __name__)

dir_path = os.path.dirname(os.path.realpath(__file__))

with open('/Users/johnnyquinn/dev/code/qwer.lol/data.json') as data:
  champ_video_hrefs = json.load(data)

@main.route('/')
def homepage():
    
    return render_template('homepage.html')

@main.route('/search', methods=['GET'])
def search():
    champ_query = request.args.get('champ_query')

    print(f'-------------------------------------------------------------------search: {champ_query}')

    return redirect(url_for('main.champ', champ=champ_query))

@main.route('/champ/<champ>')
def champ(champ):
    print(champ_video_hrefs)

    return render_template('champ.html')
