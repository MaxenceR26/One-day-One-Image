import json


def _token(token):
    with open('data/bdd.json', 'r+') as file:
        data = json.load(file)
        data['data']['token']['api_key'] = token
        file.seek(0)
        json.dump(data, file, indent=4)


def recv_token():
    with open('data/bdd.json') as file:
        data = json.load(file)

    return data['data']['token']['api_key']


def count_json():
    with open('data/bdd.json', "r+") as file:
        data = json.load(file)

    return len(data['data']['image_fav']['name'])


def recover_images():
    with open('data/bdd.json', "r+") as file:
        data = json.load(file)

    return data['data']['image_fav']['name']


def recv_image():
    with open('data/bdd.json') as file:
        data = json.load(file)

    return data['data']['image_fav']['name']


def _add_favoris(img):
    with open('data/bdd.json', 'r+') as file:
        data = json.load(file)
        x = data['data']['image_fav']['name']
        if not img in x:
            data['data']['image_fav']['name'].append(img)
            file.seek(0)
            json.dump(data, file, indent=4)


def _remove_favoris(imgs):
    with open('data/bdd.json', 'r+') as files:
        data = json.load(files)
    with open('data/bdd.json', 'w') as file:
        x = data['data']['image_fav']['name']
        if imgs in x:
            x.remove(imgs)

        data['data']['image_fav']['name'] = x
        # file.seek(0)
        json.dump(data, file, indent=4)


# Selection

def select_image(imgs):
    with open('data/bdd.json', 'r+') as file:
        data = json.load(file)
        x = data['data']['select_img']['name']
        if not imgs in x:
            data['data']['select_img']['name'].append(imgs)
            file.seek(0)
            json.dump(data, file, indent=4)


def get_select_image():
    with open('data/bdd.json', 'r+') as file:
        data = json.load(file)
    return data['data']['select_img']['name']

def get_number_select_image():
    with open('data/bdd.json', 'r+') as file:
        data = json.load(file)
        number = len(data['data']['select_img']['name'])
    return number

def remove_select_image():
    with open('data/bdd.json', 'r+') as files:
        data = json.load(files)
    with open('data/bdd.json', 'w') as file:
        x = data['data']['select_img']['name']
        x.clear()
        # file.seek(0)
        json.dump(data, file, indent=4)