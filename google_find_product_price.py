from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import requests
from bs4 import BeautifulSoup
import pymsgbox as pg
import re

szukana=pg.prompt(text='wpisz czego szukasz')
limit=pg.prompt(text='podaj kwote limitu')

while True:
    driver = webdriver.Chrome()
    driver.minimize_window()
    driver.get(f"https://www.google.com/search?q={szukana.replace(' ', '+')}")
    
    n = 5
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * n)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    time.sleep(2)

    strona=driver.page_source

    soup = BeautifulSoup(strona, "html.parser")

    for oferty in soup.find_all(class_='mnr-c pla-unit'):
        nazwa = oferty.find(class_='pymv4e').text  
        sklep = oferty.find(class_='LbUacb').text
        strona = oferty.find('a')['href']
        cena = oferty.find(class_=re.compile(r'.*e10twf T4OwTb.*')).text
        cena_liczba = float(cena.split(",")[0])
        # and sklep in ['Media Expert', 'Cortland', 'MediaMarkt.pl', 'Neonet.pl', 'RTV Euro AGD']
        if cena_liczba < float(limit)  and (szukana.lower() in nazwa.lower()):
            print(sklep,'-----',cena_liczba,'-------',nazwa.lower() )
    
    time.sleep(60)
    print('odświeżam...')
    driver.quit