import sys
import os
import time
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

dirname = 'crawled'
visited = []
queue = []
fname = 'html_f'
fnum = 0
pagesCrawled = 0
top_domain = 'edu'

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Functions
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

def crawl(page):
    global visited
    global queue
    global fnum
    global pagesCrawled

    if page in visited:
        print("Already visited")
        return
    visited.append(page)

    # Get robots.txt. Only crawl if all user agents (*) are allowed
    forbidden = []
    allowed = 0

    main_page = page.partition(top_domain)[0] + top_domain
    robots_page = main_page + '/robots.txt'

    robots = requests.get(robots_page, verify=False)
    lines = robots.text.splitlines()
    for line in lines:
        if line == 'User-agent: *':
            allowed = 1
        elif 'Disallow: ' in line:
            if line == 'Disallow: ' or line == 'Disallow:': # Blank disallow
                continue
            end = line.partition('Disallow: ')[2]
            disallowed = main_page + end
            # print(disallowed)
            forbidden.append(disallowed)
    if not allowed:
        return

    print("Crawling " + page)
    
    response = requests.get(page, verify=False)
    htmltext = response.text
    path = dirname + "/" + fname + str(fnum) + ".html"

    # Write HTML to file
    with open(path, "w", encoding="utf-8") as f:
        f.write(htmltext)
    fnum = fnum + 1
    pagesCrawled = pagesCrawled + 1

    # Extract URLs from page
    soup = BeautifulSoup(htmltext, 'lxml')
    tags = soup.find_all('a')
    for tag in tags:
        link = tag.get('href')
        if link and '.edu/' in link:
            #print(link)
            if link not in visited and link not in forbidden:
                queue.append(link)

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Main
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

if len(sys.argv) != 3:
    exit("Expected two arguments! (Name of file containing seed URLs and number of pages to crawl)")

seedfile = sys.argv[1]
numPagesStr = sys.argv[2]
numPages = int(numPagesStr)
if numPages <= 0 or numPages > 10000:
    exit("Cannot crawl " + numPagesStr + " files!")

print("Seed file: " + seedfile)
print("Number of pages to crawl: " + numPagesStr)

# Create directory to store HTML files
try:
    print("Creating directory to store HTML files...")
    os.makedirs(dirname)
except FileExistsError:
    print("Directory already exists. Deleting all files inside directory...")
    for f in os.listdir(dirname):
        os.remove(os.path.join(dirname, f))

with open(seedfile, "r") as f:
    lines = f.read().splitlines()
    # Add seed URLs to queue
    for page in lines:
        queue.append(page)

while queue:
    if pagesCrawled >= numPages:
        break
    page = queue.pop(0)
    crawl(page)
    # Don't hit server too much
    time.sleep(5)

print("Crawled " + str(pagesCrawled) + " pages!")

# Create json
intro = "{\"index\":{}}\n{\"html\": \""
html=""
outro = "\"}\n"
with open("data.json", "w") as j:
    for i in range(pagesCrawled):
        html = ""
        fname = "crawled/html_f" + str(i) + ".html"
        with open(fname, "r") as f:
            lines = f.read().splitlines()
            for line in lines:
                newLine = line.replace('\n', '')
                newLine = newLine.replace('\t', '')
                newLine = newLine.replace('\\', '')
                newLine = newLine.replace('\"', '')
                html += newLine
            j.write(intro+html+outro)
