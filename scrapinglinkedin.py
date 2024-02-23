import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import ActionChains
import traceback
from datetime import date
from unidecode import unidecode

#Inicia o webdriver
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome()

#Entra no Linkedin
navegador.get("https://www.linkedin.com/home")
navegador.maximize_window()
navegador.implicitly_wait(30)
email_element = navegador.find_element(By.ID, 'session_key')
senha_element = navegador.find_element(By.ID, 'session_password')
login_element = navegador.find_element(By.CSS_SELECTOR, '#main-content > section.section.min-h-\[560px\].flex-nowrap.pt-\[40px\].babybear\:flex-col.babybear\:min-h-\[0\].babybear\:px-mobile-container-padding.babybear\:pt-\[24px\] > div > div > form > div.flex.justify-between.sign-in-form__footer--full-width > button')

#Login e senha
email_element.send_keys('')
senha_element.send_keys('')
login_element.click()
navegador.implicitly_wait(40)

#Entra em Vagas
vagas_element = navegador.find_element(By.CSS_SELECTOR, '#global-nav > div > nav > ul > li:nth-child(3) > a')
vagas_element.click()
navegador.implicitly_wait(50)

#Procura pela vaga
navegador.find_element(By.XPATH,'/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]').send_keys('Desenvolvedor', Keys.ENTER)
navegador.implicitly_wait(50)

#Localiza lista de vagas
lista_vagas = navegador.find_element(By.CLASS_NAME,'scaffold-layout__list-container')
time.sleep(10)
links = lista_vagas.find_elements(By.TAG_NAME,'li')
abas = navegador.find_element(By.CLASS_NAME,'artdeco-pagination__pages')
lista_abas = abas.find_elements(By.TAG_NAME,'button')
lista_detalhes = navegador.find_element(By.CLASS_NAME,'scaffold-layout__detail')
titulos = []
empresas = []
regimes = []
cidades = []
Id_vaga = []
data = []
link_vaga = []

#Itera sobre as abas
for posicao in range(len(lista_abas)-1):
    try:
        abas = navegador.find_element(By.CLASS_NAME,'artdeco-pagination__pages')
        lista_abas = abas.find_elements(By.TAG_NAME,'button')
        lista_abas[posicao].click()
        links = lista_vagas.find_elements(By.TAG_NAME,'li')
        time.sleep(3)

        #Itera sobre as vagas
        for link in links:
            try:
                id = link.get_attribute('id')
                classe = link.get_attribute('class')
                if 'ember-view' in classe and 'ember' in id:
                    # print('chegou if')
                    html = link.find_element(By.TAG_NAME,'a').click()
                    links_vagas = link.find_element(By.TAG_NAME,'a').get_attribute('href')
                    time.sleep(2)
                    div = navegador.find_element(By.XPATH,'//*[@id="main"]/div/div[2]/div[1]/div')
                    ActionChains(navegador).move_to_element(div).perform()
                    navegador.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",div)

                    #Extração de dados
                    titulo_vaga = navegador.find_element(By.CLASS_NAME,'job-details-jobs-unified-top-card__job-title-link').text
                    ID_vaga = link.get_attribute('data-occludable-job-id')
                    titulo_vaga1 = unidecode(titulo_vaga)
                    empresa = link.find_element(By.CLASS_NAME,'job-card-container__primary-description').text
                    empresa1 = unidecode(empresa)
                    cidade_regime = link.find_element(By.CLASS_NAME,'job-card-container__metadata-item').text
                    cidade = re.sub(r'\([^()]*\)','',cidade_regime)
                    cidade1 = unidecode(cidade)
                    regime = re.search(r'\((.*?)\)', cidade_regime).group(1)
                    regime1 = unidecode(regime)
                    data_consulta = date.today()
                    print(titulo_vaga1)

                    #Insere nas listas
                    titulos.append(titulo_vaga1)
                    empresas.append(empresa1)
                    regimes.append(regime1)
                    cidades.append(cidade1)
                    Id_vaga.append(ID_vaga)
                    data.append(data_consulta)
                    link_vaga.append(links_vagas)
                    time.sleep(2)
            except:
                print('nao encontrou')
    except WebDriverException as erro:
        print(erro)
    time.sleep(1)

#Criação do dataframe
dictDF = {'Titulo': titulos,
            'Empresa': empresas,
            'Regime': regimes,
            'Cidade': cidades,
            'ID Vaga':Id_vaga,
            'Data': data,
            'Link': link_vaga}
df = pd.DataFrame(dictDF)
print(df)

#Exportação para excel
data_arquivo = date.today().strftime("%Y-%m-%d")
df.to_excel(f'Scraping_Linkedin_{data_arquivo}',index=False, engine='xlsxwriter')