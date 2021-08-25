from tkinter import *
import nfl_scraper
import mlb_scraper
from scrapy.crawler import CrawlerProcess
from nba_scraper.nba_scraper.spiders.nba_scraper import NbaScraper

root = Tk()


def center_window(w=300, h=200):
  # get screen width and height
  ws = root.winfo_screenwidth()
  hs = root.winfo_screenheight()
  # calculate position x, y
  x = (ws / 2) - (w / 2)
  y = (hs / 2) - (h / 2)
  root.geometry('%dx%d+%d+%d' % (w, h, x, y))


center_window(300, 140)
root.title('Sports Scrapers GUI')

button_frame = Frame(root, bg='gray')
button_frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

scraper_names = ['NFL', 'MLB', 'NBA']
scraper_files = [nfl_scraper.run, mlb_scraper.run, NbaScraper]


def find_file(scraper_name):
  if scraper_name == 'NBA':
    process = CrawlerProcess()
    process.crawl(NbaScraper)
    process.start()
  else:
    file_id = scraper_names.index(scraper_name)
    file = scraper_files[file_id]
    file()


for name in scraper_names:
  button = Button(button_frame,
                  text='Run ' + name + ' Scraper',
                  font=15,
                  bg='gray',
                  width=25,
                  pady=3,
                  command=lambda file_name=name: find_file(file_name)
                  )
  button.pack()

root.mainloop()
