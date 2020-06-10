import os
import re
import json
import time
import requests
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class wpp_bot:
    def __init__(self,bot_name):    
        self.bot = ChatBot(bot_name)
        self.trainer = ListTrainer(self.bot)
        self.driver = webdriver.Firefox()
        self.driver.get('https://web.whatsapp.com/')
        time.sleep(25)
    
    def select_tab(self,contact_name):  

        self.magnifier = self.driver.find_element_by_class_name('_3e4VU')
        self.magnifier.click()
        self.driver.implicitly_wait(15)    
        self.search_box = self.driver.find_element_by_xpath(
            "//div[@class='_2FVVk cBxw- focused']//div[@class='_3FRCZ copyable-text selectable-text']")
        self.search_box.send_keys(contact_name)
        time.sleep(3)
        self.contact = self.driver.find_elements_by_class_name("_2kHpK")
        self.contact[-1].click()
        time.sleep(2)  
    
    def apresentation(self,phrase):
                                      
        self.message_box =self.driver.find_element_by_xpath(
            "//div[@class='_2FVVk _2UL8j focused']//div[@class='_3FRCZ copyable-text selectable-text']")
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
        msg_text = post[-1].text
        return msg_text

    def  learn_Word(self,text_last,phrase,final_phrase,erro_phrase):
        self.message_box =self.driver.find_element_by_xpath(
            "//div[@class='_2FVVk _2UL8j focused']//div[@class='_3FRCZ copyable-text selectable-text']")
        self.message_box.send_keys(phrase)
        self.press_send = self.driver.find_element_by_xpath(
                    "//div[@class='_2FVVk _2UL8j focused']//div[@class='_3FRCZ copyable-text selectable-text']")
        self.press_send.send_keys(Keys.ENTER)
        self.x = True

        while self.x :
            text = self.read_msg()
            if text != text_last and re.match(r'^::',text):
                if text.find('?') != -1:
                    text_last = text
                    text = text.replace('::','')
                    text = text.lower()
                    text = text.replace("?",'?*')
                    text = text.split('*')
                    new_word = []
                    for element in text:
                        element = element.strip()
                        new_word.append(element)
                    self.trainer.train(new_word)
                    self.message_box.send_keys(final_phrase)
                    time.sleep(1)
                    self.press_send = self.driver.find_element_by_xpath(
                    "//div[@class='_2FVVk _2UL8j focused']//div[@class='_3FRCZ copyable-text selectable-text']")
                    self.press_send.send_keys(Keys.ENTER)
                    self.x = False
                    return text_last
                else:
                    self.message_box.send_keys(erro_phrase)
                    time.sleep(1)
                    self.press_send = self.driver.find_element_by_xpath(
                    "//div[@class='_2FVVk _2UL8j focused']//div[@class='_3FRCZ copyable-text selectable-text']")
                    self.press_send.send_keys(Keys.ENTER)
                    self.x = False
                    return text_last
            else:
                text_last = text
            
   
    def reply(self,text):
        reply = self.bot.get_response(text)
        reply = str(reply)
        reply = 'bot:' + reply
        self.message_box = self.driver.find_element_by_xpath(
             "//div[@class='_2FVVk _2UL8j focused']//div[@class='_3FRCZ copyable-text selectable-text']")
        self.message_box.send_keys(reply)
        time.sleep(1)
        self.press_send = self.driver.find_element_by_xpath(
            "//div[@class='_2FVVk _2UL8j focused']//div[@class='_3FRCZ copyable-text selectable-text']")
        self.press_send.send_keys(Keys.ENTER)
    
    def train_word(self,folder_name):
        for archive in os.listdir(folder_name):
            talk = open(folder_name+'/'+archive,'r').readlines()
            self.trainer.train(talk)

            