from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import datetime
import pandas
import re
import pymysql


def run():
  path = 'C:/Users/Chris/AppData/Local/Programs/Python/Python39/geckodriver'
  firefox_options = Options()
  firefox_options.add_argument("-private")
  firefox_options.headless = True
  browser = webdriver.Firefox(executable_path=path, options=firefox_options)
  url = 'https://www.pro-football-reference.com/'
  local_data = {}

  browser.get(url)
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
    data_frame = pandas.DataFrame(columns=['Team', 'Jersey_Number', 'Name', 'Position'])

    team_abrv = link[-4:-1]
    local_data[team_abrv] = []

    nfl_start_month = 8
    cur_month = datetime.date.today().month
    cur_year = datetime.date.today().year

    if nfl_start_month > cur_month:
      cur_year -= 1

    browser.get(link + str(cur_year) + '_roster.htm')
    roster_table = browser.find_element_by_id('games_played_team')
    roster_header = roster_table.find_element_by_tag_name('thead').find_element_by_tag_name('tr')
    headings = roster_header.find_elements_by_tag_name('th')
    for heading in headings:
      if heading.get_attribute('aria-label') == 'Uniform number':
        heading.click()
        break

    player_rows = []
    player_rows.insert(0, roster_table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr'))
    for player_row in player_rows[0]:
      player_data = []
      player_object = {}

      if player_row.get_attribute('class') == '':
        player_object['Team'] = team_abrv

        data = player_row.find_elements_by_tag_name('td')

        jersey_number = player_row.find_element_by_tag_name('th').text
        player_data.insert(0, jersey_number)
        player_object['Jersey_Number'] = jersey_number

        name = data[0].text
        filtered_name = re.sub('[^a-zA-Z\\s]', '', name).strip()
        player_data.insert(1, filtered_name)
        player_object['Name'] = filtered_name
        position = ''

        if data[2].text != '':
          position = data[2].text.upper()

        player_data.insert(2, position)
        player_object['Position'] = position

        local_data[team_abrv].insert((++0), player_data)
        data_frame = data_frame.append(player_object, ignore_index=True)

    connection = pymysql.connect(
      host='localhost',
      user='',
      password='',
      db='sports'
    )
    cursor = connection.cursor()
    cols = "`,`".join([str(i) for i in data_frame.columns.tolist()])
    for i, row in data_frame.iterrows():
      sql = "INSERT INTO `nfl` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
      cursor.execute(sql, tuple(row))
      connection.commit()
      print('committed a row')
    print('finished team ' + team_abrv)
