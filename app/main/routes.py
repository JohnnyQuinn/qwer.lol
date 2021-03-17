from flask import Blueprint, request, render_template, redirect, url_for, flash
from app import app 

main = Blueprint("app", __name__)

@main.route('/')
def homepage():
    
    return render_template('homepage.html')

@main.route('/search', methods=['GET'])
def search():
    champ_query = request.args.get('champ_query')

    print(f'-------------------------------------------------------------------search: {champ_query}')

    return redirect(url_for('app.champ', champ=champ_query))

@main.route('/champ/<champ>')
def champ(champ):
    
    return render_template('champ.html')
