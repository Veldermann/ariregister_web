from urllib.request import Request, urlopen
from database_connection import getDatabaseConnection
import random


eesnimed = []
perekonnanimed = []

def webScraper(top_url, list):
    url = f"{top_url}TOP"

    req = Request(
        url= url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    web_byte = urlopen(req).read()

    webpage_split = web_byte.decode('utf')
    split_one = webpage_split.split('<table class="data">')

    for x in split_one:
        split_two = x.split(f'<td class="str"><a href="{top_url}')
        for y in split_two:
            name = y.split('">')
            if '<' not in name[1].split('</a>')[0]:
                list.append(name[1].split('</a>')[0])

def writeToDatabase(isikud):
    cursor = getDatabaseConnection()
    for isik in isikud:
        cursor.execute("""
            INSERT INTO person(identification_number, name, lastname)
            VALUES (%(identification_number)s, %(name)s, %(lastname)s)
            """, {"identification_number": isik[2], "name": isik[0], "lastname": isik[1]})

def main():                
    webScraper("https://www.stat.ee/nimed/", eesnimed)
    webScraper("https://www.stat.ee/nimed/pere/", perekonnanimed)

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
                    if position == 0:
                        random_eleven += str(random.randint(3, 4))
                    else:
                        random_eleven += str(random.randint(0, 9))
                if random_eleven not in existing_elevens:
                    existing_elevens.append(random_eleven)
                    isikud.append((eesnimi, perekonnanimi, int(random_eleven)))
                    keep_looping = False
    writeToDatabase(isikud)
    return

if __name__ == '__main__':
    main()