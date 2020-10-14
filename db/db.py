from tinydb import TinyDB, Query
import pickledb
import os
# db = TinyDB('db.json')

db = pickledb.load('yt.db', True)

if not db.exists("channels"):
    db.lcreate("channels")

if not db.exists("watched"):
    db.lcreate("watched")

if not db.exists("favs"):
    db.lcreate("favs")

def get_all_channel_ids():
    return db.lgetall('channels')


def save_channel_id(channel_id):
    if not db.lexists('channels', channel_id):
        db.ladd('channels', channel_id)

def have_watched(video):
    return db.lexists('watched', video)

def save_to_watched(videos):
    for video in videos:
        if not db.lexists('watched', video):
            db.ladd('watched', video)