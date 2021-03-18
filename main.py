from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
import time

path = 'C:/Users/Chris/AppData/Local/Programs/Python/Python39/geckodriver'
firefox_options = Options()
firefox_options.add_argument("-private")
browser = webdriver.Firefox(executable_path=path, options=firefox_options)
url = 'https://www.sports-reference.com/'

browser.get(url)
browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/ul[1]/li[3]/a').click()
browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/ul[1]/li[2]/a').click()

table = browser.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/table/tbody')
rows = table.find_elements_by_css_selector('tr')
links = []

for row in rows:
  if row.get_attribute('class') == '':
    elm = row.find_element_by_css_selector('th')
    link = elm.find_element_by_tag_name('a').get_attribute('href')
    links.append(link)

for link in links:
  browser.get(link)
