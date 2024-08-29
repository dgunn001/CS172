# CS172 - Final Project (Crawler)

## Group: TeamBen15
Team member 1 - Zachary Murillo - 862008324 - zmuri001@ucr.edu  
Team member 2 - Gabriel Salazar - 861227030 - gsala005@ucr.edu  
Team member 3 - Luis Sanches    - 862046663 - lsanc044@ucr.edu  
Team member 4 - Darrien Gunn    - 862030886 - dgunn001@ucr.edu  

# Short explanation of the design
The crawler reads input from seedurls.txt, adds them to the queue, and crawls each page. Crawling a page involves reading robots.txt for which actions are allowed and adding more pages to the queue. Only pages not forbidden by robots.txt and containing a .edu domain are added.  
After crawling the specified number of web pages, a json file is generated containing all of the created HTML files. The HTML can be bulk loaded from this file by running run_json.sh.

Some important notes:
1. Per the instructor's advice, the number of levels (hops) is not taken as input.

# Required libraries
This project requires the request library for obtaining the HTML from the website. This can be installed using the following command on Mac:  
`% python3 -m pip install requests`  
The beautiful soup library is also used for obtaining URLs from the HTML document. This can be installed using the following command on Mac:  
`% python3 -m pip install beautifulsoup4`  
lxml is required for parsing the HTML with beautiful soup:  
`% python3 -m pip install lxml`

# Included files
1. README.md  
Contains information pertaining to the project.
2. crawler.py  
Contains the project crawler code.
3. seedurls.txt  
Contains the initial URLs for the crawler.
4. run_json.sh
Script that bulk loads data using data.json (created after running the crawler).
5. CS172website/
Folder that contains the website files.

# Language used
Python

# How to run the code:
To run assignment 2:  
`% python3 crawler.py <name of seed URLs file> <number of pages to crawl>`  
To bulk load data to ElasticSearch:  
`% bash run_json.sh`
