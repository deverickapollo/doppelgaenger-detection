# Doppel-Detection

Web Crawler scans the index/main page of the news website The Guardian for articles. In particular, the piece of code retrieves detailed statistics/information about news articles, e.g., title of the article, valid Uniform Resource Locators (URLs) of the article, author of the article, date of appearance, etc.  

Data persistance provided by sqlite3 database.

---
## Setup Requirements

- python3
- cyhunspell
- scrapy
- Twisted
- flask
- timeloop
- pytz
- nltk
- spacy
- language_tool_python
- numpy
- wheel

---
## Preinstallation venv setup: 

- `python3 -m venv DoppelDetect`
- `source DoppelDetect/bin/activate`
- `python3 -m pip install --upgrade pip`
  
  
## Installation:

- `python3 setup.py install`

## Uninstall:
- `pip3 uninstall DoppelDetect`

## IF NOT USING setup.py
Including system requirements, you will need these packages

Download packages from nltk:
`python3 -m nltk.downloader punkt && python3 -m nltk.downloader stopwords && python3 -m nltk.downloader averaged_perceptron_tagger`

Download spacy language packs:
`python3 -m spacy download de_core_news_sm`, `python3 -m spacy download en_core_web_sm`, `python3 -m spacy download fr_core_news_sm`, `python3 -m spacy download es_core_news_sm`

---
## Execute: 

`usage: python3 guardianbot.py [-h] [-r] [-i] [-v] [-c] [-l] [-s SIZE] [-u [USER ...]]`

optional arguments:

  -h, --help            show this help message and exit
  
  -r, --run             Run the Crawler
  
  -i, --info            Show information about the data collection
  
  -m, --mode            (Optional) Run one of the statistical modes listed below.

  -v, --version         Show version information.
  
  -c, --clean           Purge database and logs. Program exits after.
  
  -l, --log             Outputs report.log to the logs directory. Program continues.
  
  -s SIZE, --size SIZE  Output a specified number of comments for every user to CLI.
  
  -u [USER ...], --user [USER ...]
                        Output a specified number of comments from a specific user to CLI.

Modes Available:
  - char          character-level
  - vocab         vocabulary-richness
  - sentence      sentence-level   
  - leet          letspeak-based
  - white         whitespace and punctuation
  - content       content-based
  - idio          Idiosyncratic
            
Run the Bot periodically with watch: `watch -n3600 python3 guardianbot.py -r` (every hour)
                    
## Log files
1. webapp.log - Provides debug related information when running guardianbot or the webserver

---
## Testing

`pytest --html=report.html test.py`

## Notes:

Please be aware this is not production ready.  SQL queries are not sanitized and are therefore a potential security risk. Do not host live.