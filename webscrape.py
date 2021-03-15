import requests
import re
from bs4 import BeautifulSoup as bs
import pprint

pp = pprint.PrettyPrinter(indent=4)

# dictionary to be filled with champions and their abilities' demo video links 
champ_video_hrefs = {}

def get_champ_hrefs():
    """ parses through https://na.leagueoflegends.com/en-us/champions/ and
    creates a list of all the href links of all the champions """

    r = requests.get('https://na.leagueoflegends.com/en-us/champions/')

    soup = bs(r.content, features="html.parser")

    champ_links = soup.find_all('a', attrs={'class': 'style__Wrapper-sc-12h96bu-0'})

    href_list = []

    for champ in champ_links:
        href_list.append(champ['href'])

    return href_list

def get_champ_video_hrefs(href):
    """ parses through each champions info page, gets their ability video demo links and
    adds them to champ_ability_video_demo_hrefs"""

    #gets champion name from href
    champ_name = href[17:-1]

    # print(champ_name)

    #creates url based on champion
    url = 'https://na.leagueoflegends.com'+href

    r = requests.get(url)

    soup = bs(r.content, features="html.parser")

    #gets all the sources tags with type: video/mp4
    mp4_tags = soup.find_all('source', attrs={"type": "video/mp4"})

    mp4_links = []

    #sorts all mp4 links into a list 
    for mp4 in mp4_tags:
        mp4_links.append(mp4['src'])
    
    #gets all the sources tags with type: video/webm
    webm_tags = soup.find_all('source', attrs={"type": "video/webm"})

    webm_links = []

    #sorts all the sources tags with type: video/webm
    for webm in webm_tags:
        webm_links.append(webm['src'])

    add_to_champ_video_hrefs(champ_name, mp4_links, webm_links)

def add_to_champ_video_hrefs(champ_name, mp4_links, webm_links):
    """ adds champion name to champ_video_hrefs in which is a dictionary with links to mp4 and webm videos of each ability"""
    wrapper_dict = {}
    
    mp4_abilites  = {}

    webm_abilities = {}

    for link in mp4_links: 
        mp4_abilites[link[-6]] = link

    for link in webm_links: 
        webm_abilities[link[-7]] = link

    wrapper_dict['mp4'] = mp4_abilites

    wrapper_dict['webm'] = webm_abilities

    champ_video_hrefs[champ_name] = wrapper_dict

def build_champ_video_links():
    href_list = get_champ_hrefs()

    for href in href_list:
        get_champ_video_hrefs(href)

    return champ_video_hrefs

print(champ_video_hrefs)

pp.pprint(champ_video_hrefs)