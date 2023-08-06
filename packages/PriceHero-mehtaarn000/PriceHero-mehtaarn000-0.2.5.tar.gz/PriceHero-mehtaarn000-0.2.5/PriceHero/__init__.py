from PriceHero.websites import amazon as a
from PriceHero.websites import bestbuy as b
from PriceHero.websites import dell as d
from PriceHero.websites import michaels as e
from PriceHero.websites import acer as f
from PriceHero.websites import walmart as g
from PriceHero.websites import adafruit as h
from PriceHero.websites import xbox as i
from PriceHero.websites import joanns as j
from PriceHero.websites import github_shop as k
from PriceHero.websites import macys as l

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