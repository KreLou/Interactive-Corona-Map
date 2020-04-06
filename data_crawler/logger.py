import os

folder = os.path.abspath(os.path.join(os.getcwd(),'logs'))

def storeHTML(day, region, html):
    file = os.path.join(folder, '{}-{}.html'.format(region, day))
    with open(file, 'w+') as file:
        file.write(html);