import random

def generate_random_avatar(post_id, user_id):
    random.seed(post_id, user_id)
    num=random()
    with open("static\image\pic("+num+').jpg','rb') as fp:
        return fp.read()

    