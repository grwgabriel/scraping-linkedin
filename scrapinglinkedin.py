import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome()

#Entra na página

navegador.get("https://www.linkedin.com/home")
navegador.maximize_window()
navegador.implicitly_wait(30)

#Localiza elementos

email_element = navegador.find_element(By.ID, 'session_key')
senha_element = navegador.find_element(By.ID, 'session_password')
login_element = navegador.find_element(By.CSS_SELECTOR, '#main-content > section.section.min-h-\[560px\].flex-nowrap.pt-\[40px\].babybear\:flex-col.babybear\:min-h-\[0\].babybear\:px-mobile-container-padding.babybear\:pt-\[24px\] > div > div > form > div.flex.justify-between.sign-in-form__footer--full-width > button')

#Login no Linkedin

email_element.send_keys('')
senha_element.send_keys('')
login_element.click()
navegador.implicitly_wait(40)

#Localiza elementos para entrar na página de vagas

vagas_element = navegador.find_element(By.CSS_SELECTOR, '#global-nav > div > nav > ul > li:nth-child(3) > a')
vagas_element.click()
navegador.implicitly_wait(50)

#Localiza e faz a pesquisa pela vaga

navegador.find_element(By.XPATH,'/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]').send_keys('Analista de Dados', Keys.ENTER)
navegador.implicitly_wait(50)

#Localiza lista de vagas

lista_vagas = navegador.find_element(By.CLASS_NAME,'scaffold-layout__list-container')
time.sleep(10)
links = lista_vagas.find_elements(By.TAG_NAME,'li')

#Itera sobre todas as vagas

for link in links:
    try:
        id = link.get_attribute('id')
        classe = link.get_attribute('class')
        if 'ember-view' in classe and 'ember' in id:
            print('chegou if')
            html = link.find_element(By.TAG_NAME,'a').click()
        print('clicou')
        time.sleep(2)
    except:
        print('nao encontrou')