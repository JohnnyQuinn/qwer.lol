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

def interpret_tooltips(spell):
    """
        separates the tooltip (spell description) string given by the API into two parts:
            - regular strings 
            - dictionaries for custom tags and what between them (eg. '<spellPassive>Passive:</spellPassive>' gets converted into '{ 'spellPassive': 'Passive:'}')
        and puts them in order in tooltip_list
    """
    tooltip = spell['tooltip']

    tags = [
        'magicDamage',
        'physicalDamage',
        'trueDamage',
        'attackSpeed',
        'spellPassive',
        'spellActive',
        'spellName',
        'scaleArmor',
        'scaleMR',
        'scaleAD',
        'scaleMana',
        'status',
        'shield',
        'healing',
        'speed',
        'charge',
        'release',
        'recast',
        'keywordMajor',
        'keywordStealth'
    ]

    tooltip_list = []

    print ('=----------------------------------------')
    print(f'Ability name: {spell["name"]}')

    print(f'tooltip start len: {len(tooltip)}')
    print(f'original tooltip: {tooltip}')
    
    while len(tooltip) > 0:
        # if the start of tooltip isn't a tag
        if tooltip[0] != '<':
            if '<' in tooltip:
                string = tooltip[:tooltip.index('<')]
                tooltip_list.append(string)
                tooltip = tooltip.replace(string, '')
            else:
                tooltip_list.append(tooltip)
                tooltip = ''
        #if the start of tooltip isnt a line break (<br />)
        elif tooltip[:6] != '<br />':
            for tag in tags:
                if f'<{tag}' in tooltip[:tooltip.index('>')]:
                    tooltip = tooltip.replace(f'<{tag}>', '', 1)
                    tag_dict = {
                        tag: tooltip[:tooltip.index('<')]
                    }
                    tooltip = tooltip.replace(tooltip[:tooltip.index('>')+1], '', 1)
                    tooltip_list.append(tag_dict)
                    break
        elif tooltip[:4] == '<li>':
            tooltip = tooltip.replace(tooltip[:4], '', 1)
            tooltip_list.append('li')
        #if the start of tooltip is a line break (<br />)
        else:
            tooltip = tooltip.replace(tooltip[:6], '', 1)
            tooltip_list.append('br')
        print(tooltip_list)
        print(tooltip[:4])
    
    print(tooltip_list)

    tooltip_info = {
        'name': spell['name'],
        'description_list': tooltip_list
    }

    return tooltip_info


#get a list of champions from API
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

    #interpet roles for frontend
    if len(result_json['tags']) > 1:
        single_string = ''
        for tag in result_json['tags']:
            single_string += tag + ', '
        roles = single_string[:-2]
    else: 
        roles = result_json['tags'][0] 

    #interpret tooltips for frontend  
    p_tooltip = { 
        'name': result_json['passive']['name'],
        'description': result_json['passive']['description']
    }
    q_tooltip = interpret_tooltips(result_json['spells'][0])
    w_tooltip = interpret_tooltips(result_json['spells'][1])
    e_tooltip = interpret_tooltips(result_json['spells'][2])
    r_tooltip = interpret_tooltips(result_json['spells'][3])

    pp.pprint(q_tooltip)

    champ_data = {
        'name': result_json['name'],
        'roles': roles, 
        'p_mp4': champ_video_hrefs[champ.lower()]['mp4']['P'],
        'q_mp4': champ_video_hrefs[champ.lower()]['mp4']['Q'],
        'w_mp4': champ_video_hrefs[champ.lower()]['mp4']['W'],
        'e_mp4': champ_video_hrefs[champ.lower()]['mp4']['E'],
        'r_mp4': champ_video_hrefs[champ.lower()]['mp4']['R'],
        'p_tooltip': p_tooltip,
        'q_tooltip': q_tooltip,
        'w_tooltip': w_tooltip,
        'e_tooltip': e_tooltip,
        'r_tooltip': r_tooltip,
    }

    return render_template('champ.html', **champ_data)
