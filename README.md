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

`pip3 install nltk`

In python console:
`import nltk`
`nltk.download('wordnet')`
`nltk.download('punkt')`
`nltk.download('stopwords')`
`nltk.download('averaged_perceptron_tagger')`



---
## Execute: 

`usage: python3 guardianbot.py [-h] [-r] [-i] [-v] [-c] [-l] [-s SIZE] [-u [USER ...]]`

optional arguments:

  -h, --help            show this help message and exit
  
  -r, --run             Run the Crawler
  
  -i, --info            Show information about the data collection
  
  -v, --version         Show version information.
  
  -c, --clean           Purge database and logs. Program exits after.
  
  -l, --log             Outputs report.log to the logs directory. Program continues.
  
  -s SIZE, --size SIZE  Output a specified number of comments for every user to CLI.
  
  -u [USER ...], --user [USER ...]
                        Output a specified number of comments from a specific user to CLI.
                                 
Run the Bot periodicly with watch: `watch -n3600 python3 guardianbot.py -r` (every hour)
                    
## Log files
1. webapp.log - Provides debug related information when running guadianbot or the webserver

---
## Notes:

Please be aware this is not production ready.  SQL queries are not sanitized and are therefore a potential security risk. Do not host live.