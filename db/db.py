from tinydb import TinyDB, Query
import pickledb
import os
# db = TinyDB('db.json')

db = pickledb.load('yt.db', True)

if not db.exists("channels"):
    db.lcreate("channels")

def get_all_channel_ids():
    return db.lgetall('channels')


def save_channel_id(channel_id):
    if not db.lexists('channels', channel_id):
        db.ladd('channels', channel_id)

def save_test(test):
    db.insert({
        "videos": [test]
    })