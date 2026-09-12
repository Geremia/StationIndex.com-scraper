#!/usr/bin/python3

import lxml.html
import requests
import sys
import re
import csv

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <DMA name (e.g., "New York"; cf. https://www.stationindex.com/tv/tv-markets)>')
    sys.exit(1)

def getData(url):
    stations = []
    html = requests.get(url)
    doc = lxml.html.fromstring(html.content)
    table_rows = doc.xpath('//table[@class="table"]')[0]
    for r in table_rows:
        channel = r[0].cssselect('.text-bold')[0].text_content()
        callsign = r[1].text_content()
        description = r[3]
        try:
            website = description.xpath('.//a/@href')[0]
        except:
            website = ''
        power = description.xpath('.//span[contains(text(), "Station Info:")]/following-sibling::text()[1]')[0].strip()
        power = re.search(r'([0-9.]+) kW', power).group(1)
        stations.append([callsign, channel, power, website])
    return stations

url = 'https://www.stationindex.com/tv/markets/' + sys.argv[1]
stations = getData(url)

# sort stations by power (descending)
stations = sorted(stations, key=lambda x: float(x[2]), reverse=True)

csv_filename = sys.argv[1]+'.csv'
with open(csv_filename, 'w', newline='') as f:
    mywriter = csv.writer(f, delimiter='|') 
    mywriter.writerow(['Call Sign', 'Channel', 'Power (kW)', 'Website'])
    mywriter.writerows(stations)
