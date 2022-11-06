import random

def generate_random_avatar(post_id, user_id):
    random.seed(post_id, user_id)
    num=random.randint(1, 37)
    # with open(r'static/image/pic ('+str(num)+").png", 'rb') as fp:
    #     return fp.read()
    return r'static/image/pic ('+str(num)+").png"
    