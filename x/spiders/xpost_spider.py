from typing import Generator
from bs4 import BeautifulSoup
import scrapy
import pandas as pd
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

import time
import re
from x.items import XPostItem
from x.utils.content_selectors import *

class XPostSpider(scrapy.Spider):
    name = 'x'
    allowed_domains = ['www.x.com']
    # start_urls = get_postcodes()
    start_urls = ['https://x.com/YoucefZaghba/status/1847601299778343105']

    cookie = {"name": "auth_token", "value": "a1fc8b37b3d588c8ed9524bb791153c88310d006", 'domain': 'x.com'}
         

    def __init__(self, *args, **kwargs):
        super(XPostSpider, self).__init__(*args, **kwargs)
        # Set up Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        self.driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
        print("init")
        # self.driver.get("x.com")
       


    def closed(self, reason):
        # Close the WebDriver when done
        self.driver.quit()


    def get_articles(self) -> Generator[str, None, None]:
        articles =  self.driver.find_elements(By.TAG_NAME, "article")
        for article in articles:
            yield article

    def get_post_item(self, elem: WebElement, first: bool = False) -> XPostItem:
        # Get post Text
        tweetText = get_tweet_text(elem)
        isPost = first
        tweetUsername = get_tweet_username(elem)
        time_stamp = get_timestamp(elem)
        # print("stats")
        stats = get_stats(elem)
        return XPostItem(tweetText=tweetText, 
                         User_Name=tweetUsername, 
                         isPost=isPost, 
                         get_timestamp=time_stamp,
                         stats=stats)
        

    def parse_xpost(self, response: HtmlResponse):
        try:
            first = True
            for article in self.get_articles():
                post_item = self.get_post_item(article, first)
                first = False
                yield post_item  
                      

        except TimeoutException:
            print("Element not found within the given time.")

        except NoSuchElementException:
            print("Element not found within the given time.")

        except Exception as e:
            print("Parse XPOST error")
            print(e)
            # self.driver.quit()

    def wait_for_element(self, timeout=15) -> WebElement:
        elem = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//*[@data-testid='tweetText']"))  # Adjust selector
            )        
        print("loaded")



    def parse(self, response: HtmlResponse):
        print("setting cookie")
        self.driver.get(response.url)
        self.driver.add_cookie(self.cookie)
        self.driver.get(response.url)


        try:

            self.wait_for_element()

            for opt in self.parse_xpost(response):
                yield opt
            
        except TimeoutException:
            print("Element not found within the given time.")
        except Exception as e:
            print("Parse error")
            print(e)
            self.driver.quit()
            