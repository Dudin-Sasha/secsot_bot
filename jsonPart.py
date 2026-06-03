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
info = loadInfo()

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

def save_admin_profile(profile_data: dict, filename: str = "admin_profile.json"):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.extend(profile_data)
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        print("Данные успешно сохранены!")
    


    
def load_admin_profile(filename: str = "admin_profile.json") -> list:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            profile_data = json.load(file)
        print(f"Профиль успешно загружен из файла: {filename}")
        return profile_data

    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден. создан новый")
        with open(filename, "w", encoding="utf-8") as file:
             json.dump(fp=file, ensure_ascii=False, indent=4)
        with open(filename, "r", encoding="utf-8") as file:
             return json.load(file)
        # return None
    except json.JSONDecodeError:
        print(f"Ошибка: Файл '{filename}' поврежден или имеет неверный формат JSON.")
        return None
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return None
    
def reg_new_admin(cmdArg, id, admins):
    if not cmdArg:
        return ("Введите команду вместе с паролем.\nПример: `/regadmin ваш_пароль ваш_email`")

    ui = cmdArg.strip()
    user_info = ui.split()

    if user_info[0] == info['ADMIN_PASSWORD']:
        new_admin = [{"id":id,"email":user_info[1]}]
        # print(f"\n\n\n   new_admin - {new_admin} \n\n\n")
        print(type(admins))
        if len(admins)>0:
            for i in admins:
                if new_admin[0]["id"] == i["id"]:
                    print('этот профиль уже есть')
                    return "этот профиль уже есть"
                else:
                    print("этого профиля нет")
                    save_admin_profile(new_admin)
        
        print(f"Новый админ сохранен в JSON: {new_admin}. Всего админов: {len(admins)}")
        return("Вы успешно зарегистрированы как администратор! Сюда будут приходить анкеты.")
    else:
        print(user_info)
        return("Неверный пароль. Доступ заблокирован.")


