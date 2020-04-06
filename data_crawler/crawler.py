import urllib.request as request
import re

def getHTML(url):
    print('Request ' + url)
    with request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
        html = html.replace('\r', '')
        html = html.replace('\n', '')
        html = html.replace('\t', '')
        html = html.replace('  ', ' ')
        html = html.replace('&szlig;', 'ß')
        html = html.replace('&auml;', 'ä')
        html = html.replace('&Auml;', 'Ä')
        html = html.replace('&ouml;', 'ö')
        html = html.replace('&Ouml;', 'Ö')
        html = html.replace('&uuml;', 'ü')
        html = html.replace('&Uuml;', 'Ü')
        return html


def extractDate(html, regex):
    match = re.findall(regex, html)
    if len(match) > 0:
        return match[0].strip()
    return None

def extractTable(html, table, columns):
    rows = []
    match_rows = re.findall(table, html, re.M |re.I |re.S)

    for founded_row in match_rows:
        tds = re.findall(columns, founded_row, re.M | re.I|re.S)
        if len(tds) > 0:
            for i in range(0, len(tds)):
                tds[i] = tds[i].strip()
            rows.append(tds)

    return rows