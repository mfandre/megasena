import random
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import urllib.parse
from collections import OrderedDict
from tabulate import tabulate
from itertools import combinations

def getDrawInfo(q=''):
    try:
        base_url = 'https://www.google.com/search?q=megasena'+urllib.parse.quote_plus(q)
        req = Request(
            url=base_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
        )
        page = urlopen(req)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        #print(soup.prettify())

        numbers:list = getNumbers(soup)
        draw:str = getDraw(soup) # Concurso 2663 (02/12/23)
        
        return draw.split(' ')[1].strip(), numbers
    except Exception as error:
        print("Zicaaaaaaaa")
        print(error)

def getNumbers(soup:BeautifulSoup) -> list:
    numbers = soup.find_all("span", class_="zSMazd UHlKbe")
    #print(numbers)

    number_lst = []
    for number in numbers:
        #print(number.get_text())
        number_lst.append(number.get_text())

    return number_lst

def getDraw(soup:BeautifulSoup) -> str:
    draw = soup.find_all("span", class_="qLLird")
    #print(draw[0].get_text())
    return draw[0].get_text()

def getLastNDraws(n:int) -> dict:
    draw, numbers = getDrawInfo()
    # print(draw)
    # print(numbers)
    # print("---")

    data = {}
    data[draw] = numbers

    for i in range(int(draw)-(n-1), int(draw)):
        draw, numbers = getDrawInfo(' ' + i.__str__())
        data[draw] = numbers
        # print(draw)
        # print(numbers)
        # print("---")

    return data

def getAllCombinations(data:dict) -> list:
    numbers = []
    Dup = {}
    for key in data:
        for number in data[key]:
            if number in Dup:
                ItemNumber = Dup[number]
            else:
                numbers.append(number)
                Dup[number] = ItemNumber = len(numbers)-1

    combination = list(combinations(numbers, 6))
    return combination

def countNumbersInDraws(data:dict):
    count_dict = OrderedDict()
    for key in data:
        numbers = data[key]
        for number in numbers:
            if number not in count_dict:
                count_dict[number] = 1
            else:
                count_dict[number] += 1
    return count_dict

n = 3
print(f"## Last {n} draws ##")
data = getLastNDraws(n)
print(data)

print("## Count of repetions ##")
data2 = countNumbersInDraws(data)
print(tabulate(data2.items()))


print("## Random 6 games ##")
combi = getAllCombinations(data)
toPlay1 = random.randint(0, len(combi)) 
toPlay2 = random.randint(0, len(combi)) 
toPlay3 = random.randint(0, len(combi)) 
toPlay4 = random.randint(0, len(combi)) 
toPlay5 = random.randint(0, len(combi)) 
toPlay6 = random.randint(0, len(combi)) 


print(tabulate([
    combi[toPlay1],
    combi[toPlay2],
    combi[toPlay3],
    combi[toPlay4],
    combi[toPlay5],
    combi[toPlay6]
]))