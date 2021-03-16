from flask import Blueprint, request, render_template, redirect, url_for, flash
from app import app 

main = Blueprint("app", __name__)

@main.route('/')
def homepage():
    
    return render_template('homepage.html')