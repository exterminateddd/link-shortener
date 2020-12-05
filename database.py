from pymongo import MongoClient
from string import ascii_letters
from random import choice, randint


cluster = MongoClient("mongodb+srv://main_exterminated:*****@cluster0.tj4ux.gcp.mongodb.net/link-shortener"
                      "?retryWrites=true&w=majority")

links = cluster['link-shortener']['main_col']


def hash_assoc_exists(dir_hash: str) -> bool:
    return True if links.find_one({"hash": dir_hash}) else False


def link_assoc_exists(dir_url: str) -> bool:
    return True if links.find_one({"url": dir_url}) else False


def get_hash_assoc(dir_hash: str):
    return links.find_one({"hash": dir_hash})['url']


def get_link_assoc(dir_url: str):
    return links.find_one({"url": dir_url})['hash']


def insert_link(url):
    if not link_assoc_exists(url):
        new_hash = ''.join([choice(ascii_letters+"1234567890") for _ in range(randint(4, 12))])
        while hash_assoc_exists(new_hash):
            new_hash = ''.join([choice(ascii_letters + "1234567890") for _ in range(randint(4, 12))])
        links.insert_one({
            "url": url,
            "hash": new_hash
        })
        return new_hash
    else:
        return get_link_assoc(url)
