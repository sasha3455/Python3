from datetime import datetime
from abc import ABC, abstractmethod
import copy
import csv
import bcrypt

class User(ABC):
    def __init__(self, username, password, role):
        self.username = username
        self.password = self.hash_password(password)
        self.role = role
        self.created_at = datetime.now().strftime('%Y-%m-%d')

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password.encode())


    def display_info(self):
        pass

class Customer(User):
    def __init__(self, username, password):
        super().__init__(username, password, "user")
        self.history = []

    def add_to_history(self, item):
        self.history.append(item)

    def display_info(self):
        print(f"Клиент: {self.username}, История покупок: {self.history}")

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "admin")

    def display_info(self):
        print(f"Администратор: {self.username}, Доступ к управлению магазином")

class Database:

    def __init__(self):
        self._users = [
            Customer('john_doe', 'password'),
            Admin('admin_user', 'admin_password'),
        ]

        self._users[0].history = ['Кроссовки Nike', 'Ботинки Timberland']
        self._users[0].created_at = '2024-09-01'
        self._users[1].created_at = '2024-01-01'

        self._shoes = [
        {'id': 1, 'brand': 'Nike', 'model': 'Air Max', 'size': 42, 'price': 10000, 'rating': 4.5},
        {'id': 2, 'brand': 'Adidas', 'model': 'UltraBoost', 'size': 43, 'price': 12000, 'rating': 4.7},
        {'id': 3, 'brand': 'Puma', 'model': 'Speed', 'size': 40, 'price': 8000, 'rating': 4.3},
        {'id': 4, 'brand': 'Timberland', 'model': 'PRO', 'size': 44, 'price': 15000, 'rating': 4.8},
        ]
        
    def export_shoes(self, filename="shoes.csv"):
        try:
            with open(filename, mode= 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "brand", "model", "size", "price","rating"])
                for shoe in self._shoes:
                    writer.writerow([shoe['id'], shoe['brand'], shoe['model'], shoe['size'], shoe['price'], shoe['rating']])
            print(f"Данные обуви экспортированы в {filename}")
        except Exception as e:
            print(f"Ошибки при экспорте обуви: {e}")

    def import_shoes(self, filename="shoes.csv"):
        try:
            with open(filename, mode="r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self._shoes = [
                    {
                        "id": int(row['id']),
                        "brand": row["brand"],
                        "model": row["model"],
                        "size": int(row["size"]),
                        "price": float(row["price"]),
                        "rating": float(row["rating"]),
                    }
                    for row in reader
                ]
            print(f"Данные обуви загружены из {filename}")
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден. Будет создан новый при сохранении.")
        except Exception as e:
            print(f"Ошибка при загрузке обуви: {e}")

    def export_users(self, filename="users.csv"):
        try:
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["username", "password", "role", "created_at"])
                for user in self._users:
                    writer.writerow([user.username, user.password, user.role, user.created_at])
            print(f"Данные пользователей экспортированы в {filename}")
        except Exception as e:
            print(f"Ошибка при экспорте пользователей: {e}")


    def authenticate_user(self, username, password):
        for user in self._users:
            if user.username == username and user.verify_password(password):
                print("Успешный вход!")
                return True
        print("Ошибка: Неверный логин или пароль.")
        return False

    def get_users(self):
        return copy.deepcopy(self._users)

    def find_user(self, username, password):
        for user in self._users:
            if user.username == username and user.verify_password(password):
                return user
        return None

    def add_users(self, username, password, role="user"):
        if any(user.username == username for user in self._users):
            print("Ошибка: пользователь уже существует!")
            return False
        if role == "admin":
            new_user = Admin(username, password)
        else:
            new_user = Customer(username, password)
        self._users.append(new_user)
        self.export_users()
        print("Пользователь успешно добавлен!")
        return True



    def delete_user(self, username):
        self._users = [user for user in self._users if user.username != username]


    def get_shoes(self):
        return copy.deepcopy(self._shoes)

    def search_shoes(self, brand, size):
        return [shoe for shoe in self._shoes if shoe['brand'] == brand and shoe['size'] == size]
    
    def sort_shoes_by_price(self):
        return sorted(self._shoes, key=lambda shoe: shoe['price'])

   
    def add_shoe(self, brand, model, size, price, rating):
        new_shoe = {
            'id': max([shoe['id'] for shoe in self._shoes], default=0) + 1,
            'brand': brand,
            'model': model,
            'size': size,
            'price': price,
            'rating': rating,
        }
        self._shoes.append(new_shoe)
        self.export_shoes()
        print("Товар успешно добавлен!")


    def delete_shoe(self,shoe_id):
        self._shoes = [shoe for shoe in self._shoes if shoe['id'] != shoe_id]
        self.export_shoes()
        print("Товар успешно удален!")

    def show_users(self):
        for user in self._users:
            print(f"Пользователь: {user.username}, Хеш пароля: {user.password}, Роль: {user.role}")


