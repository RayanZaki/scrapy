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
import re

from nhs.items import Optician

def get_postcodes():
    postcodes = pd.read_csv('postcodes.csv')
    url = "https://www.nhs.uk/service-search/find-an-nhs-sight-test/results?SeoFriendlyUrl=find-an-nhs-sight-test&location="
    return [url + postcode for postcode in  postcodes["postcode"]]

            

class OpticianSpider(scrapy.Spider):
    name = 'optician'
    allowed_domains = ['www.nhs.uk']
    # start_urls = get_postcodes()
    start_urls = ['https://www.nhs.uk/service-search/find-an-nhs-sight-test/results?SeoFriendlyUrl=find-an-nhs-sight-test&location=E2%208AA']



    def get_opticians(self):
        elements = self.driver.find_elements(By.XPATH, "//main//ol/li")
        for elem in elements:
            yield elem

    def get_optician_url(self, elem: WebElement):
        opt = elem.find_element(By.XPATH, ".//a")

        return opt.get_attribute("href")
    
        

    def _get_name(self):
            elemHtml = self.driver.find_element(By.ID, 'page-heading').get_attribute("outerHTML")
            soup = BeautifulSoup(elemHtml, 'html.parser')
            soup.find('span').decompose()
            name = soup.get_text(' ', strip=True)
            return name
     
    def _get_address(self):
            elem = self.driver.find_element(By.XPATH, "//address[@id='address_panel_address']")
            return re.sub('\n', '', elem.text)
    
    def _get_phone(self):
            elem = self.driver.find_element(By.XPATH, "//*[@id='contact_info_panel_phone_text']")
            return elem.text
    def _get_website(self):
            try:
                elem = self.driver.find_element(By.XPATH, "//*[@id='contact_info_panel_website_link']")
                return elem.get_attribute("href")
            except NoSuchElementException:
                return
    def _get_email(self):
            try:
                elem = self.driver.find_element(By.XPATH, "//a[@id='contact_info_panel_email_link']")
                return re.sub("mailto:", "", elem.get_attribute("href"))
            except NoSuchElementException:
                return
            
    def parse_optician(self, response: HtmlResponse):
        try:
            elem = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.ID, 'page-heading'))  # Adjust selector
            ) 

            name = self._get_name()
            address = self._get_address()
            phone = self._get_phone()
            website =self._get_website()
            email = self._get_email()


            yield Optician(
                name=name,
                address=address,
                phone=phone,
                website=website,
                email=email
            )

        except TimeoutException:
            print("Element not found within the given time.")

    def parse(self, response: HtmlResponse):
        try:
            elem = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.ID, 'plan_your_journey'))  # Adjust selector
            )        


            for elem in self.get_opticians():
                url = self.get_optician_url(elem)
                if url:
                    l =  scrapy.Request(url, callback=self.parse_optician)
                    yield l
            
            
        except TimeoutException:
            print("Element not found within the given time.")
            




        # print(response.text)
        # data = response.xpath("//div[@id='plan_your_journey']")
        # self.logger.info(f"data: {data}")
        