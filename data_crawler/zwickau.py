from data_crawler import crawler, importer, logger
from corona_map.data import region_total, region_loader
from corona_map.models.import_item import  ImportItem
import datetime

def getFromList(value, list):
    for entry in list:
        if entry[0] == value:
            return entry

url = 'https://www.landkreis-zwickau.de/coronafallzahlen-landkreiszwickau';

html = crawler.getHTML(url)

date = crawler.extractDate(html, r'<p class="date"[^>]*>([^<]+)Landkreis Zwickau</p>')
dataTime = datetime.datetime.strptime(date, '%d. %B %Y')
date = dataTime.strftime('%d.%m.%Y')
print('Date: ', date)
logger.storeHTML('zwickau', date, html)


entrys = crawler.extractTable(html, r'<tr>(.*?)</tr>', r'<p.*?>([^<]+)</p.*?>')


current = importer.getCurrentStatus('zwickau.csv')

newItems = []
for entry in entrys:
    municipality = entry[0]
    amount = int(entry[1])

    old_status = getFromList(municipality, current)
    if (old_status[1] != amount):
        differenz = amount- old_status[1]
        #print(municipality, ' alt: ', old_status[1], ', neu: ', amount, ', differenz: ', differenz)
        item = ImportItem()
        item.Amount = differenz
        item.Date = date
        item.Municipality = municipality
        newItems.append(item)

if len(newItems) > 0:
    importer.storeNewItems('zwickau.csv', newItems)