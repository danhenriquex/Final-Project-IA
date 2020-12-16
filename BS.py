import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

from selenium import webdriver

import time


def get_(link):

    data = open("data.txt","a")

    page = urlopen(link)
    soup = BeautifulSoup(page, 'html.parser')

    title = soup.find(class_ = 'title')
    time = soup.find(class_ = "content-publication-data__updated")

    if title == None:
        title = soup.find(class_ = "playkit-video-info__ep-section")
        time = soup.find(class_ = "playkit-video-info__published-at")

    if title == None:

        title = soup.find(class_ = "catalog-video-title")
        time = soup.find(class_ = "catalog-metadata-published-time")

    data.write("{}\n{}\n".format(title.text, time.text))
    
    data.close()


    
def get_all(link):

    driver = webdriver.Chrome()

    driver.get(link)
    def roll():
        #Rola a barra do navegador pra baixo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Eespera 2s par rolar novamente
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    roll()
    roll()
    roll()
    

    # Pega as div's com a classe igual á abaixo
    posts = driver.find_elements_by_xpath("//div[@class='feed-post-body']")

    #salva a página html
    page_source = driver.page_source
    
    try:
        soup = BeautifulSoup(page_source, 'lxml')
    except Exception as e:
        print(e)
        
    reviews = []
    reviews_selector = soup.find_all('div', class_='feed-post-body')
    botao = soup.find_all('div', class_="load-more gui-color-primary-bg")
    botao = botao[0].a.get('href')
    print(botao)
    #try para caso de erro o selenium fechar o driver do navegador
    try:
        links = []
        i = 0
        for count, review_selector in enumerate(reviews_selector):
        
            title = review_selector.find('div', class_='feed-post-body-title gui-color-primary gui-color-hover')
            links.append(title.a.get('href'))
            print(links[i])
            get_(links[i])

            i += 1
            reviews.append(title)
        
    except Exception as e:
        print(e)
    #fecha o driver do navegador
    driver.close()
    return botao

link = "https://g1.globo.com/tudo-sobre/petrobras/"
link_vale = "https://g1.globo.com/tudo-sobre/vale/"
link_economics = "https://g1.globo.com/economia/"
link_ibm = "https://g1.globo.com/tudo-sobre/ibm/"
link_bb = "https://g1.globo.com/tudo-sobre/banco-do-brasil/"
link_oi = "https://g1.globo.com/tudo-sobre/oi/"

botao = get_all(link)

for i in range(60):

    botao = get_all(botao)

