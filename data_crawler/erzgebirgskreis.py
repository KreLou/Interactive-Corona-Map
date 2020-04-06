import sys, os
path = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.append(path)

from data_crawler import crawler, importer, logger
from corona_map.models.import_item import ImportItem

url = 'https://www.erzgebirgskreis.de/index.php?id=1126'

html = crawler.getHTML(url)

date = crawler.extractDate(html, r'<p.*?>\(Stand:[ ]+([^<]+),[ 0-9:&nbsp;Uhr]*\)</p.*?>')
print(date)

logger.storeHTML('erzgebirge', date, html)

entrys = crawler.extractTable(html, r'<tr>(.*?)</tr>', r'<td.*?>([^<]+)</td.*?>')

print(entrys)

relevant_entrys = [row for row in entrys if row[2] != '-']
newLines = []
for entry in relevant_entrys:
    item = ImportItem()
    item.Municipality = entry[0]
    item.Date = date
    item.Amount = int(entry[2].replace('+', ''))
    newLines.append(item)

importer.storeNewItems('erzgebirge.csv', newLines)