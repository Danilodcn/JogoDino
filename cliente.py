import requests
from urllib.parse import urlencode
import json
import random
import json

#from kivy.app import App

class Cliente(object):
    url = "http://daconnas.atwebpages.com/banco_de_dados.php"
    def __init__(self, nome):
        self.nome = nome

    def envia(self, metodo="GET", **kwargs):
        kwargs["nome"] = self.nome
        metodo = metodo.lower()
        if metodo == "get":
            if kwargs:
                url = self.url + "?" + urlencode(kwargs)
            else:
                url = self.url
            request = requests.get(url)
            return request
        if metodo == "post":
            request = requests.post(self.url, data=kwargs)
            return request
    
    def recebe(self):
        r = requests.get(self.url)
        return r.text


c = Cliente("Danilo Nascimento")
lista = [random.random() for i in range(30)]
txt = [f"numero_{i}" for i in range(len(lista))]
d = dict(zip(txt, lista))
r = c.envia("GET")


