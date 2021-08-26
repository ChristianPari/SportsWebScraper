from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import requests
import datetime
import pandas
import re
import pymysql


def run():
  path = 'C:/Users/Chris/AppData/Local/Programs/Python/Python39/geckodriver'
  firefox_options = Options()
  firefox_options.add_argument("-private")
  # firefox_options.headless = True
  browser = webdriver.Firefox(executable_path=path, options=firefox_options)
  url = 'https://www.baseball-reference.com/'
  local_data = {}

  browser.get(url)
  browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/ul[1]/li[2]/a').click()

  table = browser.find_element_by_xpath('/html/body/div[2]/div[5]/div[1]/div[2]/table/tbody')
  rows = table.find_elements_by_css_selector('tr')
  links = []

  for row in rows:
    if row.get_attribute('class') == '':
      elm = row.find_element_by_css_selector('.left')
      link = elm.find_element_by_tag_name('a').get_attribute('href')
      links.append(link)

  for link in links:
    data_frame = pandas.DataFrame(columns=['Team', 'Jersey_Number', 'Name', 'Position'])

    team_abrv = link[-4:-1].lower()

    if team_abrv == 'ana':
      link = re.sub('ANA', 'LAA', link)
      team_abrv = 'laa'
    if team_abrv == 'fla':
      link = re.sub('FLA', 'MIA', link)
      team_abrv = 'mia'
    if team_abrv == 'tbd':
      link = re.sub('TBD', 'TBR', link)
      team_abrv = 'tbr'

    local_data[team_abrv] = []

    mlb_start_month = 4
    cur_month = datetime.date.today().month
    cur_year = datetime.date.today().year

    if mlb_start_month > cur_month:
      cur_year -= 1

    html_text = requests.get(link + str(cur_year) + '-roster.shtml').text
    soup = BeautifulSoup(html_text, 'html.parser')
    players_table = soup.find('table', id='the40man').find('tbody')
    player_rows = players_table.find_all('tr')
    for player_row in player_rows:
      player_data = []
      player_object = {}

      player_object['Team'] = team_abrv

      number = player_row.find_all('td')[0].text
      player_data.insert(0, number)
      player_object['Jersey_Number'] = number

      player_name = player_row.find_all('td')[1].text
      player_data.insert(1, player_name)
      player_object['Name'] = player_name

      position = player_row.find_all('td')[3].text

      # BELOW WOULD BE USED TO GET SPECIFIC PLAYER POSITION DATA
      # ALTHOUGH DUE TO ITS INCREASE IN RUNTIME AND MEMORY USAGE I EXCLUDED IT FROM THE SCRAPE
      # INSTEAD THE SITE SIMPLY HAS 'POSITION' FOR PLAYERS WHO ARENT PITCHERS AND THAT IS WHAT IS PUT INTO THE DB
      # --------------------------------------------------------------------------------------------------------------
      # if position == 'Position':
      #   player_browser = webdriver.Firefox(executable_path=path, options=firefox_options)
      #   player_browser.get(link + str(cur_year) + '-roster.shtml')
      #   table = player_browser.find_element_by_id('the40man')
      #   rows = []
      #   rows.insert(0, table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr'))
      #   for row in rows[0]:
      #     player_name_row = row.find_elements_by_tag_name('td')[1].text
      #
      #     if player_name_row == player_name:
      #       row.find_elements_by_tag_name('td')[1].click()
      #       new_position = player_browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/p[1]').text
      #       # position = str(new_position).split(':')[1].strip()
      #       position = ''
      #       break
      #
      #   player_browser.close()

      player_data.insert(2, position)
      player_object['Position'] = position

      local_data[team_abrv].insert((++0), player_data)
      data_frame = data_frame.append(player_object, ignore_index=True)

    connection = pymysql.connect(
      host='localhost',
      user='root',
      password='1031GOD0623!',
      db='sports'
    )
    cursor = connection.cursor()
    cols = "`,`".join([str(i) for i in data_frame.columns.tolist()])
    for i, row in data_frame.iterrows():
      sql = "INSERT INTO `mlb` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
      cursor.execute(sql, tuple(row))
      connection.commit()
    print('finished team ' + team_abrv)
