import requests
import re
from bs4 import BeautifulSoup as bs

def get_champ_hrefs():
    """ creates a list of all the href links of all the champions """

    r = requests.get('https://na.leagueoflegends.com/en-us/champions/')

    soup = bs(r.content, features="html.parser")

    champ_links = soup.find_all('a', attrs={'class': 'style__Wrapper-sc-12h96bu-0'})

    href_list = []

    for champ in champ_links:
        href_list.append(champ['href'])