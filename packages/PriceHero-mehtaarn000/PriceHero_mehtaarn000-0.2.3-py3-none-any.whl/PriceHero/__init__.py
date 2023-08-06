from .websites import amazon as a
from .websites import bestbuy as b
from .websites import dell as d
from .websites import michaels as e
from .websites import acer as f
from .websites import walmart as g
from .websites import adafruit as h
from .websites import xbox as i
from .websites import joanns as j
from .websites import github_shop as k
from .websites import macys as l

def a(self):
    amazon_product = a.amazon(self)
    return amazon_product

def bestbuy(self):
    bestbuy_product = b.bestbuy(self)
    return bestbuy_product

def dell(dell_url):
    dell_product = d.dell(dell_url)
    return dell_product

def michaels(michaels_url):
    michaels_product = e.michaels(michaels_url)
    return michaels_product

def acer(acer_url):
    acer_product = f.acer(acer_url)
    return acer_product

def walmart(walmart_url):
    walmart_product = g.walmart(walmart_url)
    return walmart_product

def adafruit(adafruit_url):
    adafruit_product = h.adafruit(adafruit_url)
    return adafruit_product

def xbox(xbox_url):
    xbox_product = i.xbox(xbox_url)
    return xbox_product

def joanns(joanns_url):
    joanns_product = j.joanns(joanns_url)
    return joanns_product

def github_shop(github_shop_url):
    github_shop_product = k.github_shop(github_shop_url)
    return github_shop_product

def macys(macys_url):
    macys_product = l.macys(macys_url)
    return macys_product