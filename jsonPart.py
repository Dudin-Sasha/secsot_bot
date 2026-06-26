import json
import os
import re
from datetime import datetime

def loadInfo(filename: str = "Data.json") -> dict:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            profile_data = json.load(file)

        print(f"Профиль успешно загружен из файла: {filename}")
        # print(profile_data)
        return profile_data
    except:
        print("не загрузить импортировать данные")
        return None
__info = loadInfo()

def dateCheck(date_str):
    if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", date_str):
        return False
    try:
        date_str = datetime.strptime(date_str, "%d.%m.%Y")
        if (date_str <= datetime.now()):
            return True  
        else:
            return False
    except ValueError:
        return False

def cardcheck(card_number: str) -> bool:
    card_number = re.sub(r'\D', '', card_number)
    if not (13 <= len(card_number) <= 19):
        return False
        
    total = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1
    
    for count in range(num_digits):
        digit = int(card_number[count])
        if not ((count & 1) ^ oddeven):
            digit = digit * 2
            if digit > 9:
                digit = digit - 9
        total += digit
    return (total % 10) == 0



    


def load_admin_profile(filename: str = "admin_profile.json") -> list:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            profile_data = json.load(file)
        print(f"Профиль успешно загружен из файла: {filename}")
        return profile_data

    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден. создан новый")
        with open(filename, "w", encoding="utf-8") as file:
             json.dump(fp=file, ensure_ascii=False, indent=4, obj="{}")
        with open(filename, "r", encoding="utf-8") as file:
             return json.load(file)
        # return None
    except json.JSONDecodeError:
        print(f"Ошибка: Файл '{filename}' поврежден или имеет неверный формат JSON.")
        return None
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return None


def save_admin_profile(profile_data: list):
    with open(file="admin_profile.json", mode='w', encoding='utf-8') as file:
        json.dump(obj=profile_data, fp=file, ensure_ascii=False, indent=4)
        print(f"profile data - {profile_data}\nfile - {file}")
        print("Данные успешно сохранены!")


def reg_new_admin(cmdArg, TG_id = -1, Max_id = -1):
    if not cmdArg:
        return ("Введите команду вместе с паролем.\nПример: `/regadmin ваш_пароль ваш_email`")
    user_info = cmdArg.strip().split()
    if len(user_info) <= 1:
        return ("Введите команду вместе с паролем.\nПример: `/regadmin ваш_пароль ваш_email`")

    admins = load_admin_profile()

    print(f"user info - {user_info}\nadmins - {admins}")
    if user_info[0] == __info['ADMIN_PASSWORD']:
        new_admin = {"TG_id":TG_id,"Max_id":Max_id,"email":user_info[1]}

        if len(admins)>0:
            for i in admins:
                if new_admin["email"] == i["email"]:
                    if TG_id != -1 and i["TG_id"] == -1:
                        new_admin = {"TG_id":TG_id,"Max_id":i["Max_id"],"email":user_info[1]}
                        admins.remove(i)


                    elif Max_id != -1 and i["Max_id"] == -1:
                        new_admin = {"TG_id":i["TG_id"],"Max_id":Max_id,"email":user_info[1]}
                        admins.remove(i)
                    else:
                        return("Этот профиль уже есть")
        
        admins.append(new_admin)


        save_admin_profile(profile_data=admins)
        print(f"Новый админ сохранен в JSON: {new_admin}. Всего админов: {len(admins)}")
        return("Вы успешно зарегистрированы как администратор! Сюда будут приходить анкеты.")
    else:
        print(user_info)
        return("Неверный пароль. Доступ заблокирован.")




# --- Пример интеграции в вашу систему отправки почты ---
# file_path = "user_video.mp4" # или "user_photo.jpg"
# media_bytes, media_type = get_media_bytes_and_type(file_path)

# if media_bytes:
#     print(f"Файл успешно прочитан. Тип: {media_type}")
#     # Передаем байты и MIME-тип в вашу функцию отправки:
#     my_email_sender(media_bytes, media_type)
