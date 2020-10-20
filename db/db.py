from tinydb import TinyDB, Query
import pickledb
import os
# db = TinyDB('db.json')
path = os.path.join(os.path.abspath('.'), 'yt.db')
db = pickledb.load(path, True)

if not db.exists("channels"):
    db.lcreate("channels")

if not db.exists("watched"):
    db.lcreate("watched")

if not db.exists("favs"):
    db.lcreate("favs")

def get_all_channels():
    return db.lgetall('channels')


def save_channel(channel):
    if not db.lexists('channels', channel):
        db.ladd('channels', channel)

def have_watched(video):
    return db.lexists('watched', video)

def save_to_watched(videos):
    for video in videos:
        if not db.lexists('watched', video):
            db.ladd('watched', video)

def pop_from_list(list_name, pos):
    return db.lpop(list_name, pos)