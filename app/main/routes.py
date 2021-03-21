from flask import Blueprint, request, render_template, redirect, url_for, flash
from app import app 
import json
import os
import pprint
import requests

pp = pprint.PrettyPrinter(indent=4)

main = Blueprint("main", __name__)

with open('./data.json') as data:
  champ_video_hrefs = json.load(data)

def handle_request(extension): 
    """ handles requests to Riot API """

    url = 'http://ddragon.leagueoflegends.com/cdn/11.6.1/data/en_US/'

    url += extension + '.json'

    params = {
        'X-Riot-Token': 'RGAPI-939795eb-3003-4d13-9b85-693dc223cd08'
    }

    result_json = requests.get(url, params=params).json()
    result_json = result_json['data']

    return result_json

champ_list = handle_request('champion')

@main.route('/')
def homepage():
    """ serves homepage.html """
    
    return render_template('homepage.html')

@main.route('/search', methods=['GET'])
def search():
    """ handles search querys inputted into searchbar"""

    champ_query = request.args.get('champ_query')

    print(f'-------------------------------------------------------------------search: {champ_query}')

    return redirect(url_for('main.champ', champ=champ_query))

@main.route('/champ/<champ>')
def champ(champ):
    """ serves champ.html and handles API requests for champion """

    result_json = handle_request('champion/' + champ)
    result_json = result_json[champ]

    if len(result_json['tags']) > 1:
        single_string = ''
        for tag in result_json['tags']:
            single_string += tag + ', '
        roles = single_string[:-2]
    else: 
        roles = result_json['tags'][0]  

    champ_data = {
        'name': result_json['name'],
        'roles': roles, 
        'champ_p_mp4': champ_video_hrefs[champ.lower()]['mp4']['P'],
        'champ_q_mp4': champ_video_hrefs[champ.lower()]['mp4']['Q'],
        'champ_w_mp4': champ_video_hrefs[champ.lower()]['mp4']['W'],
        'champ_e_mp4': champ_video_hrefs[champ.lower()]['mp4']['E'],
        'champ_r_mp4': champ_video_hrefs[champ.lower()]['mp4']['R'],
        'champ_p_tooltip': result_json['passive']['description'],
        'champ_q_tooltip': result_json['spells'][0]['tooltip'],
        'champ_w_tooltip': result_json['spells'][1]['tooltip'],
        'champ_e_tooltip': result_json['spells'][2]['tooltip'],
        'champ_r_tooltip': result_json['spells'][3]['tooltip'],
    }

    
    return render_template('champ.html', **champ_data)
