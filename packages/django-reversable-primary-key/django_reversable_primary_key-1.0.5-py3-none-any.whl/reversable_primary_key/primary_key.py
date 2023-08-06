import random
import time

START_TIME = 1588568377822

def make_id():
    '''
    inspired by http://instagram-engineering.tumblr.com/post/10853187575/sharding-ids-at-instagram
        '''

    return to_id(time.time())


def to_id(unix_epoch):
    t = int(unix_epoch*1000) - START_TIME
    u = random.SystemRandom().getrandbits(23)
    id = (t << 23 ) | u

    return id

def reverse_id(id):
    if isinstance(id, str):
        id = int(id)
    t  = id >> 23
    return (t + START_TIME)/1000