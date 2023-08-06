# coding: utf-8
# Author：KZ

import base64

import requests


class Irecognition():
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"

    def __init__(self, client_id='P0DVZvEnkdlRoqgGvY3EkZic', client_secret='YiExSSoyFs65QfKlHMjpoTGPtOgDoLdx'):
        '''
        get_token:[调用鉴权接口获取的token]
        :param client_id: 官网获取的AK
        :param client_secret: 官网获取的SK
        '''
        self.host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
                    'client_id={client_id}&client_secret={client_secret}'.format(client_id=client_id, client_secret=client_secret)
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
        }
        self.request_url = self.request_url + "?access_token=" + self.__get_token()

    def __get_token(self):
        try:
            response = requests.get(self.host,
                                    headers = {
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
                                    },
                                    proxies = {'http': None, 'https': None}
                                    )
            data = response.json()
            token = data.get('access_token')
            return token
        except BaseException as e:
            raise BaseException(e)

    def get_image(self, path):
        '''
        二进制方式打开图片文件
        :param path:
        :return:
        '''
        f = open(path, 'rb')
        img = base64.b64encode(f.read())
        f.close()
        params = {"image": img}
        try:
            return self.__result_process(params=params)
        except BaseException as e:
            raise BaseException(e)

    def __result_process(self, params):
        response = requests.post(self.request_url, data=params, headers=self.headers,proxies = {'http': None, 'https': None}).json()

        class KZ():
            @property
            def raw(self):
                return response

            @property
            def wordslist(self):
                words_result = response.get('words_result')
                words_list = []
                for i in words_result:
                    words_list.append(i.get('words'))
                return words_list

            @property
            def words(self):
                words_result = response.get('words_result')
                words = ''
                for i in words_result:
                    words += i.get('words')
                return words

        kz = KZ()
        return kz


if __name__ == '__main__':
    ocr = Irecognition()
    data = ocr.get_image('kz.jpg')
    print(data.words)
