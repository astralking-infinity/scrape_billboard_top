#!/usr/bin/python
# scrape_billboard_top.py - The program extracts data of today's top 100
# music from http://billboard.com/charts/hot-100

import os
import requests
import xlsxwriter
from bs4 import BeautifulSoup
from datetime import datetime

url = 'http://billboard.com/charts/hot-100'

month = '%02d' % datetime.now().month
day = '%02d' % datetime.now().day
year = '%d' % datetime.now().year
filename = 'billboardhot100_' + year + '.xlsx'
sheetname = 's' + month + day

directory = 'billboard100'

# Create directory
if not os.path.exists(directory):
    os.makedirs(directory)
os.chdir(os.path.join(os.getcwd(), directory))

# Create spreadsheet file
workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet(sheetname)
bold = workbook.add_format({'bold': True})

# Fill in the headers
worksheet.write(0, 0, 'Top', bold)
worksheet.write(0, 1, 'Artist', bold)
worksheet.write(0, 2, 'Song', bold)

# Download webpage
print('Downloading webpage...', url)
response = requests.get(url)
response.raise_for_status
print('Done.')

# Parse html
print('Parsing...')
soup = BeautifulSoup(response.content, 'html.parser')
print('Done.')

print('Extracting data...')

containers = soup.find_all('div', {'class': 'container'})

real_len = 0
for container in [containers[5], containers[7]]:
    articles = container.find_all('article')
    for i in range(len(articles)):
        rank = articles[i].find('span')
        if not rank:
            continue
        real_len += 1
        rank = rank.text
        artist = articles[i].find('a').text.strip()
        if not artist:
            artist = articles[i].find('h3').text.strip()
        song = articles[i].find('h2').text
        print(rank + ', ' + artist + ', ' + song)

        worksheet.write(real_len, 0, rank)
        worksheet.write(real_len, 1, artist)
        worksheet.write(real_len, 2, song)

print('Done.')

workbook.close()
print('Saved to...', os.path.join(os.getcwd(), directory, filename))
