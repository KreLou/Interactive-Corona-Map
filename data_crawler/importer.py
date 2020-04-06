import os
import pandas

path = os.path.join(os.getcwd(), '..', 'corona_map', 'database')

def storeNewItems(filename, newItems):
    filename = os.path.realpath(os.path.join(path, filename))
    print('Save ', len(newItems), ' in ', filename)
    with open(filename, 'r+', encoding='utf-8') as file:
        found = False
        for line in file:
            if line.startswith(newItems[0].Date):
                found = True
        if not found:
            for item in newItems:
                string = '{};{};{}\n'.format(item.Date, item.Municipality.strip(), item.Amount)

                file.write(string)
        else:
            print('Day ', newItems[0].Date, ' allready saved')


def getCurrentStatus(filename):
    filename = os.path.realpath(os.path.join(path, filename))
    print('Load: ', filename)
    df = pandas.read_csv(filename, delimiter=';', encoding='utf-8')
    grouped = df.groupby(['Region']).sum()['Anzahl']
    grouped = grouped.reset_index()
    return grouped.values.tolist()