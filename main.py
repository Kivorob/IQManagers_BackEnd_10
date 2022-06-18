import vk_api
import json
from config import token


session = vk_api.VkApi(token = token)
vk = session.get_api()


# Функция загрузки мемов из альбома
def get_photo_from_album(owner_id, album_id, rev, extended, count):

    data = vk.photos.get(owner_id = owner_id, album_id = album_id, rev = rev, extended = extended, count = count)
    return data


# Функция записи полученных данных на json-файл
def write_data_to_json(data):

    with open("IQManagers_BackEnd_db.json", "w") as db:
        json.dump(data, db)


# Функция взятия имени по id
def get_fistname_by_id(user_id):

    namedata = vk.users.get(user_ids = user_id, name_case = "nom")
    return namedata[0]["first_name"]

# Функция взятия фамилии по id
def get_lastname_by_id(user_id):

    namedata = vk.users.get(user_ids = user_id, name_case = "nom")
    return namedata[0]["last_name"]


# Функция вывода имени-фамилии пользователя и количества лайков под фото
def create_custom_json(owner_id, album_id, rev, extended, count):

    dataset = get_photo_from_album(owner_id, album_id, rev, extended, count)

    resDataset = {"count": 0, "items": []}


    album_id = 0
    photo_id = 0
    photo_url = ""
    text = ""
    user_id = 0
    user_first_name = ""
    user_last_name = ""
    count_likes =  0

    resDataset["count"] = dataset["count"]

    for data in dataset["items"]:

        buffer = dict(album_id = data["album_id"],
                      photo_id = data["id"],
                      photo_url = data["sizes"][3]["url"],
                      text = data["text"],
                      user_id = data["user_id"],
                      user_first_name = get_fistname_by_id(data["user_id"]),
                      user_last_name = get_lastname_by_id(data["user_id"]),
                      count_likes = data["likes"]["count"]
                      )
        resDataset["items"].append(buffer)


    return resDataset



def write_result(dataset):
    with open("IQManagers_BackEnd_10_jsonres.json", 'w') as dt:
        json.dump(dataset, dt)

    with open("IQManagers_BackEnd_10_res.txt", "w") as f:
        for data in dataset["items"]:
            f.write(data["user_first_name"] + " " + data["user_last_name"] + " has " + str(data["count_likes"]) + " likes for the meme\n")



owner_id = -197700721
album_id = 283939598
rev = 1
extended = 1
count = 1000

data = get_photo_from_album(owner_id, album_id, rev, extended, count)
write_data_to_json(data)

resData = create_custom_json(owner_id, album_id, rev, extended, count)
write_result(resData)