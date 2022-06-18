import vk_api
import json
from config import token
import random

session = vk_api.VkApi(token=token)
vk = session.get_api()


# Функция загрузки мемов из альбома
def get_photo_from_album(owner_id, album_id, rev, extended, count):
    data = vk.photos.get(owner_id=owner_id, album_id=album_id, rev=rev, extended=extended, count=count)
    return data


# Функция записи полученных данных на json-файл
def write_data_to_json(data):
    with open("IQManagers_BackEnd_db.json", "w") as db:
        json.dump(data, db)


# Функция взятия имени по id
def get_fistname_by_id(user_id):
    namedata = vk.users.get(user_ids=user_id, name_case="nom")
    return namedata[0]["first_name"]


# Функция взятия фамилии по id
def get_lastname_by_id(user_id):
    namedata = vk.users.get(user_ids=user_id, name_case="nom")
    return namedata[0]["last_name"]


# Функция вывода имени-фамилии пользователя и количества лайков под фото
def create_custom_json(owner_id, album_id, rev, extended, count):
    dataset = get_photo_from_album(owner_id, album_id, rev, extended, count)

    resDataset = {"count": 0, "items": []}

    resDataset["count"] = dataset["count"]

    for data in dataset["items"]:

        buffer_count_likes = data["likes"]["count"]
        buffer_count_likes = int(buffer_count_likes)

        buffer = dict(album_id=data["album_id"],
                      owner_id=data["owner_id"],
                      photo_id=data["id"],
                      photo_url=data["sizes"][3]["url"],
                      text=data["text"],
                      user_id=data["user_id"],
                      user_first_name=get_fistname_by_id(data["user_id"]),
                      user_last_name=get_lastname_by_id(data["user_id"]),
                      count_likes=buffer_count_likes
                      )
        resDataset["items"].append(buffer)

    return resDataset


# Функция для записи результатов задания 1
def write_result(dataset):
    with open("IQManagers_BackEnd_10_jsonres.json", 'w') as dt:
        json.dump(dataset, dt)

    with open("IQManagers_BackEnd_10_res.txt", "w") as f:
        for data in dataset["items"]:
            f.write(data["user_first_name"] + " " + data["user_last_name"] + " has " + str(
                data["count_likes"]) + " likes for the meme\n")


# Функция "лайк"
def add_like(data):
    data["count_likes"] = vk.likes.add(type="photo", owner_id=data["owner_id"], item_id=data["photo_id"])
    return data


# Функция "скип" по факту убирает лайк
def delete_like(data):
    data["count_likes"] = vk.likes.delete(type="photo", owner_id=data["owner_id"], item_id=data["photo_id"])
    return data


# Консольный интерфейс для проверки работоспособности функций "лайк" и "скип"
def view_photos():
    with open("IQManagers_BackEnd_10_jsonres.json", "r") as f:
        dataset = json.load(f)

        command = ''

        for i in range(0, dataset["count"]):

            while command != 'l' and command != 's' and command != 'e':
                print("meme in this URL: " + dataset["items"][i]["photo_url"])

                if dataset["items"][i]["text"] != '':
                    print(dataset["items"][i]["text"])

                print("if you like the meme then send l")
                print("if you do not like meme then send s")
                print("if you want to stop watch memes then send e")
                command = input()

            if command == 'l':
                dataset["items"][i] = add_like(dataset["items"][i])

            if command == 's':
                dataset["items"][i] = delete_like(dataset["items"][i])

            if command == 'e' or i == dataset["count"] - 1:
                break

            command = ''

    with open("IQManagers_BackEnd_10_jsonres.json", "w") as f:
        json.dump(dataset, f)


# Функция для вывода в консоль постов, которые не являются конкурентными (может и более мощные)
def print_photo(photo, flag, l):
    if flag == "promoted":
        print("promoted meme URL: " + photo["photo_url"])
        l += ("promoted meme URL: " + photo["photo_url"] + "\n")

        if photo["text"] != '':
            print("promoted text: " + photo["text"])
            l += ("promoted text: " + photo["text"] + "\n")

        print("promoted count likes: " + str(photo["count_likes"]))
        l += ("promoted count likes: " + str(photo["count_likes"]) + "\n")

    else:
        print("meme URL: " + photo["photo_url"])
        l += ("meme URL: " + photo["photo_url"] + "\n")

        if photo["text"] != '':
            print("text: " + photo["text"])
            l += ("text: " + photo["text"] + "\n")

        print("count likes: " + str(photo["count_likes"]))
        l += ("count likes: " + str(photo["count_likes"]) + "\n")

    l += "\n"
    return l


# Консольное отображение ранжирование мемов, при котором со 100% вероятностью будут выводится мемы,
# у которых не более 80% от количества лайков продвигаемого мема, остальные же будут выводиться
# с меньшей вероятностью случайно, чем больше лайков от количества продигаемого мема, тем меньше вероятность

def ranging_photo(pp):

    logs = ""

    with open("IQManagers_BackEnd_10_jsonres.json", "r") as f:

        dataset = json.load(f)


        logs = print_photo(pp, "promoted", logs)


        for i in range(0, dataset["count"]):

            if dataset["items"][i]["count_likes"] * 10 <= pp["count_likes"] * 8:
                logs = print_photo(dataset["items"][i], "", logs)

            else:
                if random.randint(0, 101) <= 50 * pp["count_likes"] / dataset["items"][i]["count_likes"]:
                    logs = print_photo(dataset["items"][i], "", logs)

    with open("IQManagers_BackEnd_30_ranging_list.txt", "w") as f:
        f.write(logs)


owner_id = -197700721
album_id = 283939598
rev = 1
extended = 1
count = 1000

promoted_photo = {
    "album_id": 283939598,
      "owner_id": -197700721,
      "photo_id": 457240792,
      "photo_url": "https://sun5-3.userapi.com/impg/tewldJUxJGB_98K5ehYLPyN_o1EgaMgcO4-9Cw/OoKcuyPYbpk.jpg?size=807x454&quality=95&sign=804057510c8ad4d54c09ad48ee1cf6f0&c_uniq_tag=Mio3XAyBu9BRQ5hGceDw3n9z9uxAKUGCrlzVaAHWpZg&type=album",
      "text": "",
      "user_id": 202328127,
      "user_first_name": "\u041a\u0441\u0435\u043d\u0438\u044f",
      "user_last_name": "\u041c\u0438\u0446\u0443\u043a\u043e\u0432\u0430",
      "count_likes": 2
                }

random.seed(version=2)

# data = get_photo_from_album(owner_id, album_id, rev, extended, count)
# write_data_to_json(data)
#
# resData = create_custom_json(owner_id, album_id, rev, extended, count)
# write_result(resData)

# view_photos()


ranging_photo(promoted_photo)
