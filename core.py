# encoding=utf8
import requests
from wox import Wox
from lxml import etree
import time
import pyperclip


class Main(Wox):

    def request(self, url):
        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
        header = {"User-Agent": ua}
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http": "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port")),
                "https": "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))}
            return requests.get(url, proxies=proxies, headers=header)
        else:
            return requests.get(url, headers=header)

    def query(self, key):

        if key == '':
            return [{
                "Title": 'Synonymer',
                "SubTitle": 'input words to find its Synonyms and Antonyms',
                "IcoPath": "image/icon.ico",
            }]

        if len(key.split(':')) == 2:
            code = key.split(':')[1]
        else:
            code = True

        url = 'https://www.thesaurus.com/browse/' + key.split(':')[0]

        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
        header = {"User-Agent": ua}
        time.sleep(0.5)  # avoid ban by website

        web_content = requests.get(url, headers=header).content
        t_web_content = etree.HTML(web_content)

        result = {'sy': [], 'an': []}
        word_number = 0
        word_exist = True

        while word_exist:
            word_number += 1
            addr_sy = '//*[@id="initial-load-content"]/main/section/section/div[2]/section/ul/li[' + str(
                word_number) + ']/span/a/text()'
            addr_an = '//*[@id="initial-load-content"]/main/section/section/div[3]/section/ul/li[' + str(
                word_number) + ']/span/a/text()'
            word_sy = t_web_content.xpath(addr_sy)
            word_an = t_web_content.xpath(addr_an)
            if word_sy != []:
                result['sy'].append(word_sy[0])
            if word_an != []:
                result['an'].append(word_an[0])
            word_exist = word_sy != [] or word_an != []

        return_para = []

        if code == 'a' or code == True:
            for i in result['sy']:
                return_para.append(
                    {
                        "Title": i,
                        "SubTitle": 'Synonyms',
                        "IcoPath": "image/sy.ico",
                        "JsonRPCAction": {
                            "method": "inClipBoard",
                            "parameters": [i],
                            "dontHideAfterAction": True
                        }
                    }
                )

        if code == 's' or code == True:
            for i in result['an']:
                return_para.append(
                    {
                        "Title": i,
                        "SubTitle": 'Antonyms',
                        "IcoPath": "image/an.png",
                        "JsonRPCAction": {
                            "method": "inClipBoard",
                            "parameters": [i],
                            "dontHideAfterAction": True
                        }
                    }
                )

        if code != 's' and code != 'a' and code != True:
            return [{
                "Title": 'Synonymer',
                "SubTitle": 'Wrong parameter, only support "s" and "a"',
                "IcoPath": "image/icon.ico",
            }]

        return return_para

    def inClipBoard(self, word):
        pyperclip.copy(word)


if __name__ == "__main__":
    Main()
