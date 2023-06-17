from db_connect import connect_db as db
import sql_command as sql
import hashlib
import string


# хеширование пароля
def password_hash(password_sha):
    bytes_password = bytes(password_sha.encode("utf-8"))
    password_sha = hashlib.sha256(bytes_password).hexdigest()
    return password_sha


# регистрация пользователя sql запрос
def registration_sql(login_reg, password_reg):
    last_row_users_db = db(sql.last_row(), "select")
    if len(last_row_users_db) == 0:
        db(sql.registration(login_reg, password_reg, 0), "")
    else:
        db(sql.registration(login_reg, password_reg, last_row_users_db[0][0]), "")
    return True


"""
Блок для регистрации пользователя
"""


def registration(login_reg, password_reg):
    # проверка на существующие пользователи в БД по логину
    login_check = db(sql.check_login(login_reg), "select")
    if len(login_check) == 0:
        # хеширование пароля
        password_reg = password_hash(password_reg)
        # sql запрос на регистрацию пользователя
        registration_sql(login_reg, password_reg)
        print("Спасибо за регистрацию в системе")
    else:
        print("Такой пользователь уже существует!")


"""
Блок для входа пользователя
"""


def sign_in(login_sign, password_sign):
    login_sign = db(sql.check_login(login_sign), "select")
    if len(login_sign) == 0:
        print("Введены не корректные данные!")
    else:
        password_sign = password_hash(password_sign)
        chek_password = db(sql.check_password(login_sign[0][0]), "select")
        if chek_password[0][0] != password_sign:
            print("Введены не корректные данные!")
        else:
            print("Добро пожаловать в систему!")


"""
Блок добавления бинарника c семплами пользователя
"""
def add_sample (file):
    buometry_samle = db(sql.add_sampe_sql(file), "")


"""
Блок выборки семплом по пользователю
"""
def select_sample ():
    sample = db(sql.select_sample_sql(), "select_sample")
    return sample

"""
if __name__ == "__main__":
    # вход или регистрация в системе
    action = int(input("1 - вход в систему\n2 - регистрация в системе\n"))
    if action == 1:
        # пользователь вводит логин и пароль
        login = input("Введите логин: ").translate({ord(c): None for c in string.whitespace})
        password = input("Введите пароль: ").translate({ord(c): None for c in string.whitespace})
        sign_in(login, password)
    if action == 2:
        # пользователь вводит логин и пароль
        login = input("Введите логин: ").translate({ord(c): None for c in string.whitespace})
        password = input("Введите пароль: ").translate({ord(c): None for c in string.whitespace})
        registration(login, password)
"""