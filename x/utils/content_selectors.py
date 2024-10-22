

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


def get_tweet_text(elem: WebElement) -> str:
    el = elem.find_element(By.XPATH, ".//*[@data-testid='tweetText']")
    return el.get_attribute("innerText")

def get_tweet_username(elem: WebElement) -> str:
    el = elem.find_element(By.XPATH, ".//*[@data-testid='User-Name']//a")
    link = el.get_attribute("href")
    return link.split("/")[-1]

def get_timestamp(elem: WebElement) -> str:
    el = elem.find_element(By.XPATH, ".//time")
    return el.get_attribute("innerText")


def get_stats(elem: WebElement) -> str:
    el = elem.find_element(By.XPATH, ".//div[@aria-label and not(@aria-label='Image')]")
    string = el.get_attribute("aria-label")
    return string