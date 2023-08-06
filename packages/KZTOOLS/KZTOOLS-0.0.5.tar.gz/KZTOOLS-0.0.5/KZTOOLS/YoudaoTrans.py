# coding: utf-8
# Author：KZ

import requests

from .FakeUseragent import UserAgent


class Translator():
    def __init__(self):
        self.url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"

    def translate(self, text):
        headers = {"User-Agent": UserAgent().random()}
        formdata = {
            'i': text,
            'from': "AUTO",
            'to': "AUTO",
            'smartresult': "dict",
            "doctype": "json",
            "keyfrom": "fanyi.web",
        }
        response = requests.post(url=self.url, headers=headers, data=formdata)

        class KZ():
            @property
            def raw(self):
                return response

            @property
            def json(self):
                return response.json()

            @property
            def text(self):
                return response.json().get('translateResult', [[{}]])[0][0].get('tgt', '')

        kz = KZ()
        return kz


if __name__ == '__main__':
    translator = Translator()
    data = translator.translate('我爱中国！')
    print(data)
    print(data.raw)
    print(data.raw.text)
    print(data.json)
    print(data.text)
