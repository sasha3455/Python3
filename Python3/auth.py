from database import Database

db = Database()
users = db.get_users()

def authenticate_user(username, password):
    try:
        return next((user for user in db.get_users() if user['username'] == username and user['password'] == password and user['role'] == 'user'), None)
    except Exception as e:
        print(f"Ошибка аутентификации: {e}")
        return None

def authenticate_admin(username, password):
    try:
        return next((user for user in db.get_users() if user['username'] == username and user['password'] == password and user['role'] == 'admin'), None)
    except Exception as e:
        print(f"Ошибка аутентификации: {e}")
        return None