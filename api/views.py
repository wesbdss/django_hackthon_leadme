
from django.contrib.auth.models import User
from app.models import Leads
from rest_framework import viewsets
from api.serializers import UserSerializer,LeadsSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import time
import pickle


driver = None
options = Options()
options.headless = False
# precisa do firefox instalado na maquina
driver = webdriver.Firefox(options=options,executable_path=GeckoDriverManager().install())
driver.get('https://www.linkedin.com/')
cookies = pickle.load(open("./api/cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get('https://www.linkedin.com/')
# 
# driver.implicitly_wait(2)
# username = driver.find_element_by_id('username')
# username.send_keys('<seu email do linkedin>')
# password = driver.find_element_by_id('password')
# password.send_keys('<sua senha do linkedin>')
# button = driver.find_element_by_class_name('btn__primary--large')
# button.click()  
# driver.implicitly_wait(2)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class LeadsViewSet(viewsets.ViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    """
{
    "empresa":"NAScon"
}
    """

    def create(self, request, format=None):
        entrada = request.data
        global driver
        
        driver.get("https://www.linkedin.com/search/results/companies/")
        driver.implicitly_wait(3)
        empresa = entrada['empresa']
        empresaobj = {"nome":empresa}
        button_serch = driver.find_element_by_tag_name('input')
        button_serch.click()
        driver.implicitly_wait(1)
        button_serch.send_keys(Keys.CONTROL + "a")
        button_serch.send_keys(Keys.DELETE)
        time.sleep(2)
        button_serch.send_keys(empresa)
        time.sleep(2)
        button_serch.send_keys(Keys.ENTER)
        time.sleep(2)
        
        pagina = driver.find_element_by_class_name("entity-result__title-text").find_element_by_class_name("app-aware-link")
        time.sleep(2)
        driver.get(pagina.get_attribute("href"))

        
        empresaobj['link'] = driver.current_url
        ops = [x for x in driver.find_elements_by_class_name("org-page-navigation__item-anchor") if x.text == "Pessoas"]
        # driver.get(driver.find_element_by_xpath("//html/body/div[6]/div[3]/div/div/div/div[2]/main/div[1]/section/div/div[2]/div[1]/div[2]/div/a").get_attribute('href'))
        ops[0].click()
        # 
        lim = 2

        for _ in range(lim):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            driver.implicitly_wait(2)
        driver.implicitly_wait(5)
        lista = driver.find_element_by_xpath("//html/body/div[6]/div[3]/div/div/div/div[2]/main/div[2]/div/div[2]/div/ul").find_elements_by_tag_name('li')
        # Limite de páginas pra procurar
        lista_nao_checada = []
        for pessoa in lista:
            """
                {
                    "identificado": bool,
                    "nome": string,
                    "cargo": string,
                    "contato": string,
                }
            """
            doc = {}
            if pessoa.find_element_by_class_name("artdeco-entity-lockup__title").text != "Usuário do LinkedIn":
                doc['identificado'] = True
                doc['nome'] = pessoa.find_element_by_class_name("artdeco-entity-lockup__title").text
            else:
                doc['identificado'] = False
            doc['cargo'] = pessoa.find_element_by_class_name("artdeco-entity-lockup__subtitle").text
            lista_nao_checada.append(doc)


        for pessoa in lista_nao_checada:
            try:
                driver.get("https://www.google.com.br/")
                driver.find_element_by_class_name("gLFyf").send_keys('"'+pessoa['cargo']+'"' + ' linkedin ' )
                driver.find_element_by_class_name("gLFyf").send_keys(Keys.ENTER)
                driver.find_element_by_class_name('yuRUbf').click()
                driver.implicitly_wait(2)
                if driver.find_element_by_class_name("text-body-medium").text == pessoa['cargo']:
                    print("é a pessoa")
                    pessoa['nome'] = driver.find_element_by_tag_name('h1').text
                    pessoa['url'] = driver.current_url
                    
                    if len(Leads.objects.filter(nome =pessoa['nome'],cargo = pessoa['cargo'])) >= 1:
                        print("Lead Confirmado e ja existir")
                    else:
                        print("Lead Confirmado")
                        Leads.objects.create(empresa=empresa,nome =pessoa['nome'],cargo = pessoa['cargo'],link=pessoa['url'])
                else:
                    print("Lead Não Confirmado")
            except Exception as x:
                print("deu Merda ",x)
        
        return Response(lista_nao_checada)
    

   

  
