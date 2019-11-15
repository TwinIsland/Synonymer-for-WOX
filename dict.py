import requests
from lxml import etree


def search_AnSy(word):
    url = 'https://www.thesaurus.com/browse/' + word

    ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    header = {"User-Agent": ua}

    web_content = requests.get(url,headers=header).content
    t_web_content = etree.HTML(web_content)


    result = {'sy':[],'an':[]}
    word_number = 0
    word_exist = True

    while word_exist:
        word_number += 1
        addr_sy = '//*[@id="initial-load-content"]/main/section/section/div[2]/section/ul/li['+ str(word_number) +']/span/a/text()'
        addr_an = '//*[@id="initial-load-content"]/main/section/section/div[3]/section/ul/li['+ str(word_number) +']/span/a/text()'
        word_sy = t_web_content.xpath(addr_sy)
        word_an = t_web_content.xpath(addr_an)
        if word_sy != []:
            result['sy'].append(word_sy[0])
        if word_an != []:
            result['an'].append(word_an[0])
        word_exist = word_sy != [] or word_an != []


    print(result)