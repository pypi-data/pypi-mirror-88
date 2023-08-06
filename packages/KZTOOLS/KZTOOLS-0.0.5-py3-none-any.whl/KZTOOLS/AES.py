# coding: utf-8
# Author：KZ
# Crypto:pycryptodome

import base64
import random

from Crypto.Cipher import AES


class AESCrypto():

    def pkcs7padding(self, text):
        """
        明文使用PKCS7填充
        最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
        :param text: 待加密内容(明文)
        :return:
        """
        bs = AES.block_size  # 16
        length = len(text)
        bytes_length = len(bytes(text, encoding='utf-8'))
        # tips：utf-8编码时，英文占1个byte，而中文占3个byte
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
        padding_text = chr(padding) * padding
        return text + padding_text

    def pkcs7unpadding(self, text):
        """
        处理使用PKCS7填充过的数据
        :param text: 解密后的字符串
        :return:
        """
        length = len(text)
        unpadding = ord(text[length - 1])
        return text[0:length - unpadding]

    def encrypt(self, key, content, iv):
        """
        AES加密
        key,iv使用同一个
        模式cbc
        填充pkcs7
        :param key: 密钥
        :param content: 加密内容
        :return:
        """
        key_bytes = bytes(key, encoding='utf-8')
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        # 处理明文
        content_padding = self.pkcs7padding(content)
        # 加密
        encrypt_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
        # 重新编码
        result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        return result

    def decrypt(self, key, content, iv):
        """
        AES解密
         key,iv使用同一个
        模式cbc
        去填充pkcs7
        :param key:
        :param content:
        :return:
        """
        key_bytes = bytes(key, encoding='utf-8')
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        # base64解码
        encrypt_bytes = base64.b64decode(content)
        # 解密
        decrypt_bytes = cipher.decrypt(encrypt_bytes)
        # 重新编码
        result = str(decrypt_bytes, encoding='utf-8')
        # 去除填充内容
        result = self.pkcs7unpadding(result)
        return result

    def get_key(self, n):
        """
        获取密钥 n 密钥长度
        :return:
        """
        c_length = int(n)
        source = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
        length = len(source) - 1
        result = ''
        for i in range(c_length):
            result += source[random.randint(0, length)]
        return result


if __name__ == '__main__':
    # {"code":"0","massage":"成功","data":[{"cet01":"202006","cet02":"YYTHUMAN3 ","cet03":"23              ","cet04":"Y","cet05":null,"cet06":"CMGX15(L10 系統組裝部)","cet07":"D","cet08":"S0230804","cet09":"王福寅                  ","cet10":"5A        ","cet11":"11.00","cet12":"213.35","cet13":"0.00","cet14":"0.00","cet15":"0.00","cet16":"0.00","cet17":"213.35","cet18":"0.00","cet19":"213.35","cet20":null,"cet21":null,"cet22":null,"cet23":null,"cet24":null,"cet25":null,"cet26":null,"cet27":null,"cet28":null,"cet29":null,"cet30":null,"cet31":null,"cet32":null,"cetacti":null,"cetuser":null,"cetgrup":null,"cetmodu":null,"cetdate":null}]}
    aes_key = "9966d405dcbe8397"
    aes_iv = b'0535039203920535'
    source_en = 'zmMMh+OS4iw+AEQxOrvHUq7arAq8YqO8/EmmhmZD+B0XmZPZf7wVxiomjKnz2bVZRfL4H8LhlW8k/psQol//mx0Ev/STTK5cjRJyvzhZHveDqVAaiqag9fyCpAHN2rU+2K2L/JROlp71Noy0cwr1bLRjQHPAZed8MZ8YltInFp9dZSX5WEOFb8VH71Dhbs6zHO5CkAGrLBstdVf9K3ryPf0ZktqXJB8we9bCP0mpA3KrhasLF2Ifd/YYcms8uAum2Yde33xLdpr82k5RkgMGZwQ1JK78VBawmsqm75lleXiLYQXrZGq4PCQ1eDL1jSb4zkGXH8t/RlI0jgAiS/ETkjP6vi6DKXZrNJLvDsRGJXoGAbuaybPUCwsDYn+XP6xsTKeHAopC9O/Vt6fe4wQl7aASPEFwJdP2LrDphQS8VV0UNTM7ZswwblGxMx7A4MWFURtP5DEdpFym1LLImsW/7Rh6NBJWJ6ESbU12C16h63irWrdJAqpyINBFGqrki5QrOEzQTApPYtHcCKua1jDapq/1ix+Kbw1bTTSS2xOrLGz/werAZVPeLbNmc332m3M5xAttvZxw/VUKwMDLHNMRWA0vdIOx7SoJxAlvthb03sz9jNYwppbWkM8IpnPzQF05wyn1PuWK37nQwBj/M8nbWBfEQ+u1acY3DaD5IzqYRLpMTAhvfbOx+rL/Mn5PAo+40Sjsyp7jCCdL9KrhYrji9ST08VGL7anlB8p5XPfMwx3ygm2XfQIZ70+H3uYC0cEPFdfXZ8QKDuIb1KDh+ewVGZEDWbxs9N2lp4mOPvUFTTMZJm9+K7+PXiEB6WhPws47yLRZX7LoVB+oI67hC5r8qZUOExcGRHo1b0oxn2JuyuQ='
    # 解密
    aes = AESCrypto()
    res = aes.decrypt(aes_key, source_en, aes_iv)
    print(res)
