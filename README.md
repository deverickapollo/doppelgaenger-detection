# Doppel-Detection

Web Crawler scans the index/main page of the news website The Guardian for articles. In particular, the piece of code retrieves detailed statistics/information about news articles, e.g., title of the article, valid Uniform Resource Locators (URLs) of the article, author of the article, date of appearance, etc.  

Data persistance provided by sqlite3 database.

---
## Setup Requirements

`pip3 install scrapy`

`pip3 install Twisted`

`pip3 install flask`

`pip3 install timeloop`

`pip3 install pytz`

---
## Execute: 

`FLASK_APP=webserver.py FLASK_ENV=development flask run`
---
## Log files
1. webapp.log - Provides debug related information when running guadianbot or the webserver
2. report.log - Provides statistical and analytical information related to articles and comments published to the Guardian website.

---
## Notes:

Please be aware this is not production ready.  SQL queries are not sanitized and are therefore a potential security risk. Do not host live.