from urllib.request import Request, urlopen
import random


eesnimed = []
perekonnanimed = []

def webScraper(top_url):
    url = f"{top_url}TOP"

    req = Request(
        url= url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    web_byte = urlopen(req).read()

    webpage_split = web_byte.decode('utf')
    asd1 = webpage_split.split('<table class="data">')

    for x in asd1:
        asd2 = x.split(f'<td class="str"><a href="{top_url}')
        #print(asd2)
        for y in asd2:
            asd3 = y.split('">')
            if '<' not in asd3[1].split('</a>')[0]:
                if "pere" in url:
                    perekonnanimed.append(asd3[1].split('</a>')[0])
                else:
                    eesnimed.append(asd3[1].split('</a>')[0])
                
webScraper("https://www.stat.ee/nimed/")
webScraper("https://www.stat.ee/nimed/pere/")

isikud = []
existing_elevens = []
count = 1
for eesnimi in eesnimed:
    for perekonnanimi in perekonnanimed:
        keep_looping = True
        while keep_looping == True:
            count += 1
            random_eleven = ""
            for position in range(11):
                random_eleven += str(random.randint(0, 9))
            if random_eleven not in existing_elevens:
                existing_elevens.append(random_eleven)
                isikud.append((eesnimi, perekonnanimi, random_eleven))
                keep_looping = False
                
# TODO! Persons to database

""" READ .INI
import configparser

config = configparser.ConfigParser()
config.read('FILE.INI')
print(config['DEFAULT']['path'])     # -> "/path/name/"
config['DEFAULT']['path'] = '/var/shared/'    # update
config['DEFAULT']['default_message'] = 'Hey! help me!!'   # create

with open('FILE.INI', 'w') as configfile:    # save
    config.write(configfile)
"""