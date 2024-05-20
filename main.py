import re
from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, contract_address

# Инициализация подключения к локальному узлу Ethereum
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Доступ к смарт-контракту
contract = w3.eth.contract(address=contract_address, abi=abi)

# Словарь для хранения учетных данных пользователей
users = {
    "0xadmin": {"username": "admin", "password": "123"},
    "0xbubuk": {"username": "bubuk", "password": "1234"}
}

# Словарь для хранения записей о недвижимости
real_estate_records = {
    1: {
        "owner": "0xadmin",
        "address": "г. Москва, Классенская улица, 8",
        "description": "Просторный дом с 4 спальнями и большим садом.",
        "status": "available"
    },
    2: {
        "owner": "0xbubuk",
        "address": "г. Москва, Суперская улица, 12",
        "description": "Квартира в центре города с великолепным видом.",
        "status": "available"
    }
}

# Словарь для хранения объявлений о продаже недвижимости
real_estate_listings = {
    1: {
        "property_id": 1,
        "owner": "0xadmin",
        "price": "500000",
        "description": "Продается просторный дом с большим садом.",
        "status": "active"
    },
    2: {
        "property_id": 2,
        "owner": "0xbubuk",
        "price": "300000",
        "description": "Квартира в центре города с великолепным видом.",
        "status": "active"
    }
}

# Функция для проверки сложности пароля
def is_strong_password(password):
    if len(password) < 12:
        print("Пароль должен быть не менее 12 символов.")
        return False
    if not re.search(r"[A-Z]", password):
        print("Пароль должен содержать хотя бы одну заглавную букву.")
        return False
    if not re.search(r"[a-z]", password):
        print("Пароль должен содержать хотя бы одну строчную букву.")
        return False
    if not re.search(r"[0-9]", password):
        print("Пароль должен содержать хотя бы одну цифру.")
        return False
    if not re.search(r"[!@#\$%\^&\*]", password):
        print("Пароль должен содержать хотя бы один специальный символ (!, @, #, $, %, ^, &, *).")
        return False
    if re.search(r"(password|123456|qwerty|abc123)", password, re.IGNORECASE):
        print("Пароль не должен содержать простые шаблоны.")
        return False
    return True

# Функция для регистрации пользователя
def register():
    print("Регистрация:")
    public_key = input("Введите публичный ключ вашего аккаунта: ")
    if public_key in users:
        print("Этот аккаунт уже зарегистрирован.")
        return
    
    username = input("Введите ваше имя пользователя: ")
    while True:
        password = input("Введите ваш пароль: ")
        if is_strong_password(password):
            break
        else:
            print("Попробуйте снова.")
    
    # Сохранение учетных данных пользователя
    users[public_key] = {"username": username, "password": password}
    print(f"Создан новый аккаунт: {public_key}")

# Функция для авторизации пользователя
def login():
    print("Авторизация:")
    public_key = input("Введите публичный ключ вашего аккаунта: ")
    password = input("Введите ваш пароль: ")

    # Логика проверки учетных данных
    if public_key in users and users[public_key]["password"] == password:
        print(f"Вы успешно вошли в систему с адресом: {public_key}")
        return public_key
    else:
        print("Неверный публичный ключ или пароль. Попробуйте снова.")
        return None

# Функция для создания записи о недвижимости
def create_real_estate_record(user):
    print("Создание записи о недвижимости:")
    record_id = len(real_estate_records) + 1
    property_address = input("Введите адрес недвижимости: ")
    property_description = input("Введите описание недвижимости: ")

    real_estate_records[record_id] = {
        "owner": user,
        "address": property_address,
        "description": property_description,
        "status": "available"
    }

    print(f"Запись о недвижимости успешно создана с ID: {record_id}")

# Функция для создания объявления о продаже недвижимости
def create_real_estate_listing(user):
    print("Создание объявления о продаже недвижимости:")
    listing_id = len(real_estate_listings) + 1
    property_id = int(input("Введите ID недвижимости: "))
    
    if property_id not in real_estate_records:
        print("Недвижимость с указанным ID не существует.")
        return
    
    if real_estate_records[property_id]['owner'] != user:
        print("Вы не являетесь владельцем данной недвижимости.")
        return
    
    price = input("Введите цену продажи: ")
    description = input("Введите описание объявления: ")

    real_estate_listings[listing_id] = {
        "property_id": property_id,
        "owner": user,
        "price": price,
        "description": description,
        "status": "active"
    }

    print(f"Объявление о продаже недвижимости успешно создано с ID: {listing_id}")

# Функция для изменения статуса недвижимости
def change_real_estate_status(user):
    print("Изменение статуса недвижимости:")
    property_id = int(input("Введите ID недвижимости: "))
    
    if property_id not in real_estate_records:
        print("Недвижимость с указанным ID не существует.")
        return
    
    if real_estate_records[property_id]['owner'] != user:
        print("Вы не являетесь владельцем данной недвижимости.")
        return
    
    new_status = input("Введите новый статус (available/sold): ")
    if new_status not in ["available", "sold"]:
        print("Недопустимый статус.")
        return
    
    real_estate_records[property_id]['status'] = new_status
    print(f"Статус недвижимости с ID: {property_id} успешно изменен на {new_status}")

# Функция для изменения статуса объявления о продаже недвижимости
def change_listing_status(user):
    print("Изменение статуса объявления о продаже недвижимости:")
    listing_id = int(input("Введите ID объявления: "))
    
    if listing_id not in real_estate_listings:
        print("Объявление с указанным ID не существует.")
        return
    
    if real_estate_listings[listing_id]['owner'] != user:
        print("Вы не являетесь владельцем данного объявления.")
        return
    
    new_status = input("Введите новый статус (active/inactive): ")
    if new_status not in ["active", "inactive"]:
        print("Недопустимый статус.")
        return
    
    real_estate_listings[listing_id]['status'] = new_status
    print(f"Статус объявления с ID: {listing_id} успешно изменен на {new_status}")

# Функция для покупки недвижимости
def buy_real_estate(user):
    print("Покупка недвижимости:")
    listing_id = int(input("Введите ID объявления о продаже: "))
    
    if listing_id not in real_estate_listings:
        print("Объявление с указанным ID не существует.")
        return
    
    listing = real_estate_listings[listing_id]
    property_id = listing["property_id"]
    owner = listing["owner"]
    
    if listing["status"] != "active":
        print("Это объявление не активно.")
        return
    
    if owner == user:
        print("Вы не можете купить собственную недвижимость.")
        return
    
    # Выполнение покупки: смена владельца недвижимости и изменение статуса объявления и недвижимости
    real_estate_records[property_id]['owner'] = user
    real_estate_records[property_id]['status'] = "sold"
    real_estate_listings[listing_id]['status'] = "inactive"
    
    print(f"Вы успешно купили недвижимость с ID: {property_id} по объявлению с ID: {listing_id}")

# Функция для вывода средств
def withdraw_funds(user):
    print("Вывод средств:")
    amount = int(input("Введите сумму для вывода (в wei): "))
    
    try:
        tx_hash = contract.functions.withdraw(amount).transact({'from': user})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        if receipt.status == 1:
            print(f"Вы успешно вывели {amount} wei.")
        else:
            print("Ошибка при выводе средств.")
    except Exception as e:
        print(f"Ошибка: {e}")

# Функция для получения информации о доступных недвижимостях
def view_available_real_estate():
    print("Доступные недвижимости:")
    for record_id, record in real_estate_records.items():
        if record["status"] == "available":
            print(f"ID: {record_id}, Адрес: {record['address']}, Описание: {record['description']}, Владелец: {record['owner']}")

# Функция для получения информации о текущих объявлениях о продаже недвижимости
def view_active_listings():
    print("Текущие объявления о продаже недвижимости:")
    for listing_id, listing in real_estate_listings.items():
        if listing["status"] == "active":
            print(f"ID: {listing_id}, ID недвижимости: {listing['property_id']}, Цена: {listing['price']}, Описание: {listing['description']}, Владелец: {listing['owner']}")

# Функция для получения информации о балансе на смарт-контракте
def view_contract_balance(user):
    try:
        balance = contract.functions.balanceOf(user).call()
        print(f"Ваш баланс на смарт-контракте: {balance} wei")
    except Exception as e:
        print(f"Ошибка: {e}")

# Функция для получения информации о балансе на аккаунте
def view_account_balance(user):
    try:
        balance = w3.eth.get_balance(user)
        print(f"Ваш баланс на аккаунте: {balance} wei")
    except Exception as e:
        print(f"Ошибка: {e}")

# Функция для отображения меню и обработки выбора пользователя
def main_menu():
    current_user = None

    while True:
        print("\nГлавное Меню")
        if current_user:
            print(f"Вы вошли как: {users[current_user]['username']}")
            print("1. Создать запись о недвижимости")
            print("2. Создать объявление о продаже недвижимости")
            print("3. Изменить статус недвижимости")
            print("4. Изменить статус объявления о продаже недвижимости")
            print("5. Купить недвижимость")
            print("6. Вывести средства")
            print("7. Просмотр доступных недвижимости")
            print("8. Просмотр текущих объявлений о продаже недвижимости")
            print("9. Просмотр баланса на смарт-контракте")
            print("10. Просмотр баланса на аккаунте")
            print("11. Выйти")
        else:
            print("1. Регистрация")
            print("2. Авторизация")
            print("3. Выйти")
        
        choice = input("Введите ваш выбор: ")
        
        if current_user:
            try:
                if choice == '1':
                    create_real_estate_record(current_user)
                elif choice == '2':
                    create_real_estate_listing(current_user)
                elif choice == '3':
                    change_real_estate_status(current_user)
                elif choice == '4':
                    change_listing_status(current_user)
                elif choice == '5':
                    buy_real_estate(current_user)
                elif choice == '6':
                    withdraw_funds(current_user)
                elif choice == '7':
                    view_available_real_estate()
                elif choice == '8':
                    view_active_listings()
                elif choice == '9':
                    view_contract_balance(current_user)
                elif choice == '10':
                    view_account_balance(current_user)
                elif choice == '11':
                    print("Выход...")
                    current_user = None
                else:
                    print("Недопустимый выбор. Попробуйте снова.")
            except Exception as e:
                print(f"Ошибка: {e}")
        else:
            if choice == '1':
                register()
            elif choice == '2':
                current_user = login()
            elif choice == '3':
                print("Выход...")
                break
            else:
                print("Недопустимый выбор. Попробуйте снова.")

# Запуск главного меню
main_menu()
