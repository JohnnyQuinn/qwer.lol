import requests
import re
from bs4 import BeautifulSoup as bs

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
    source_tags = soup.find_all('source', attrs={"type": "video/mp4"})

    mp4_links = []

    #sorts all mp4 links into a list 
    for source in source_tags:
        mp4_links.append(source['src'])

    print(mp4_links)

def add_to_champ_video_hrefs(mp4_links):
    for link in mp4_links:
        if link[-6] == 'P': 






get_champ_video_hrefs('/en-us/champions/leona/')