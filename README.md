# SportsWebScraper

The goal of this project was to enhance my skils of web scraping by opening myself up to unfamiliar frameworks and libraries. Which I choose to create 3 scrapers for the major professional sport leagues data (NFL, MLB and NBA) which retrieve their teams and players from a [sports site](http://sports-reference.com) and writes to a csv file for each league and specific team.

### Added Feature

After I completed this task I created a MySQL database that is hosted on AWS and insert the scraped data into to the database
for the NFL and MLB scrapers, then with the NBA scraper I used CSV reader to read the files that the program generated
for each team and insert the row data into the database.

## Technologies

I used 3 web sracping tools during this project:

- [Selenium](https://www.selenium.dev/)
- [Scrapy](https://scrapy.org/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Tinkter](https://docs.python.org/3/library/tkinter.html)
    - I used this to create a simple GUI to simply run and select which scraper the user desires to run

## What I Learned

There can be A LOT that goes into a web scraping project and the technology you want to use varies depending on what
website data you are working with and what you want to do with it.

- I found that BeautifulSoup is the easiest and most straight-forward to use. Its 'html parser' tool makes extracting
  specific data from HTML or XML very easy.
- Unlike BS4, Scrapy has built-in tools for extracting data from HTMLs, and in turn proved to have much better
  performance time than all three of the tools I used. Not only fast but it consumes a lot less memory and CPU usage
  than other libraries and tools out there.
- Lastly Selenium. Not everyone knows this (including me at first since I had never heard of it before) but it is
  actually used for automated testing for Web Applications, a way for devs to write tests for their sites. In short, its
  ability to perform browser automation allows us to use search sites for the data we wish to extract but at the cost of
  speed. Due to the full automation of the technology, it is substantially slower than the other two tools I used.

## Challenges Faced

Considering I went into this project not even knowing about Selenium and Scrapy, and only hearing of BeautifulSoup4; I
knew this was going to be a lot of researching and document checking to see how I was supposed to create these scrapers.

- Mostly trying to break down the use of going through the HTML data and elements to find the specifics of what I was
  trying to extract
- Utilizing session points / the ability to go deep into one links data but go back to the original point of entry to
  select another teams data

## In The End

This project was a huge success, it runs smoothly with all three tools (although like stated, Seleniums takes a heavy
bit of CPU and time to execute) and writes to CSV files that could in fact later be used to store in a database to be
used for an API of my own I create. Not to say I have mastered these tools but now I do have the reference for them and
ability to look over my work when in need to scrape data in the future.
