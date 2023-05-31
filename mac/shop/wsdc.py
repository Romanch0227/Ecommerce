




def key_genarate(id):
    number = '0123456789'
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    id = ''
    for i in range(0, 10, 2):
        id += random.choice(number)
        id += random.choice(alpha)
    return id