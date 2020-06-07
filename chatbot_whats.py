import os
import time
import re
import requests
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



# Crianda a classe wppbot que será responsável pela interação do bot com whatsapp
class wpp_bot:
    # Retorna o caminho do diretório atual
    dir_path = os.getcwd()

    # função que sempre é chamada quando se cria uma instância da classe
    def __init__(self,bot_name):    
        # Atribuindo um nome do bot    
        self.bot = ChatBot(bot_name)
        # Permite o chat bot ser treinando com um lista de strings
        # A lista representa uma conversa
        self.trainer = ListTrainer(self.bot)

        # Cria uma instância da API de automação do Firefox
        self.driver = webdriver.Firefox()
    
    def select_tab(self,contact_name):
        # Falando para o webdriver abrir o site  do wpp
        self.driver.get('https://web.whatsapp.com/')
        # Falando pro webdriver esperar '10' para passar ao próximo comando
        time.sleep(25)
        # Seleciona o elemento da lupa
        self.magnifier = self.driver.find_element_by_class_name('_3e4VU')
        # Clicka no elemento da lupa
        self.magnifier.click()
        self.driver.implicitly_wait(15)    

        # Pegando a tag que fornece o nome da pessoa que quero falar
        self.search_box = self.driver.find_element_by_xpath(
            "//div[@class='_2FVVk cBxw- focused']//div[@class='_3FRCZ copyable-text selectable-text']")
        # Enviando o nome selecionado para  a caixa de pesquisa
        self.search_box.send_keys(contact_name)
        time.sleep(3)
        # Pega o nome que foi encontrado pela caixa de busca
        self.contact = self.driver.find_elements_by_class_name("_2kHpK")

        # Clika no elemento que foi encontrado na caixa de busca
        self.contact[-1].click()
        time.sleep(2)  
    
    def apresentation(self,phrase):
                                      
        # Achando a caixa para de mensagem                        
        self.message_box =self.driver.find_element_by_xpath(
            "//div[@class='_2FVVk _2UL8j focused']//div[@class='_3FRCZ copyable-text selectable-text']")
        # verificando se é phrase é do tipo list
        if type(phrase) == list:
            for frase in phrase:
                self.message_box.send_keys(frase)
                time.sleep(1)
                self.press_send = self.driver.find_element_by_xpath(
                    "//div[@class='_2FVVk _2UL8j focused']//div[@class='_3FRCZ copyable-text selectable-text']")
                self.press_send.send_keys(Keys.ENTER)
                time.sleep(2)
        else:
            return False
    def read_msg(self):
        time.sleep(5)
        post = self.driver.find_elements_by_class_name("eRacY")
        msg_text = post[-2].text
        return msg_text