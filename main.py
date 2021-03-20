from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
import time
import pandas

path = 'C:/Users/Chris/AppData/Local/Programs/Python/Python39/geckodriver'
firefox_options = Options()
firefox_options.add_argument("-private")
browser = webdriver.Firefox(executable_path=path, options=firefox_options)
url = 'https://www.sports-reference.com/'

local_data = {}
data_frame = pandas.DataFrame(columns=['Number', 'Name', 'Position'])

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
  team_abrv = link[-4:-1]
  browser.get(link + '2020_roster.htm')
  roster_table = browser.find_element_by_id('games_played_team')
  roster_header = roster_table.find_element_by_tag_name('thead').find_element_by_tag_name('tr')
  headings = roster_header.find_elements_by_tag_name('th')
  for heading in headings:
    if heading.get_attribute('aria-label') == 'Uniform number':
      heading.click()

  player_rows = roster_table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
  for player_row in player_rows:

    if player_row.get_attribute('class') == '':
      data = player_row.find_elements_by_tag_name('td')
      name = data[0].text
      local_data[name] = {}

      uniform_number = player_row.find_element_by_tag_name('th').text
      local_data[name]['Number'] = uniform_number

      position = data[2].text.upper()
      local_data[name]['Position'] = position

      local_data[name]['Team'] = team_abrv

print(local_data)
