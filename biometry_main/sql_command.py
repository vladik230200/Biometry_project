import psycopg2

# получает id последнего пользователя в БД
def last_row():
    last_row_db = "SELECT \"ID_USER\" " \
                  "FROM \"USERS\"" \
                  "ORDER BY \"ID_USER\" DESC " \
                  "LIMIT 1"
    return last_row_db


# запрос в БД за логином
def check_login(login):
    login_id = "SELECT \"LOGIN\" " \
               "FROM \"USERS\" " \
               "WHERE \"LOGIN\" = '" + login + "'"
    return login_id


# запрос в БД пароля по логину
def check_password(login):
    password = "SELECT \"PASSWORD\" " \
               "FROM \"USERS\" " \
               "WHERE \"LOGIN\" = '" + login + "'"
    return password

# sql запросы для регистрации пользователя
def registration(login, password, last_row_db):
    # если БД пустая, то регистрирует первого пользователя
    if last_row_db == 0:
        registration_user = "INSERT INTO \"USERS\" " \
                            "(\"ID_USER\", \"LOGIN\", \"PASSWORD\", \"BIOMETRY_USE\")" \
                            " VALUES ('1', '" + str(login) + "', '" + str(password) + "', 'False');"
        return registration_user
    # регистрирует пользователя с инкрементом ID_USER + 1
    else:
        registration_user = "INSERT INTO \"USERS\" " \
                            "(\"ID_USER\", \"LOGIN\", \"PASSWORD\", \"BIOMETRY_USE\")" \
                            " VALUES ('" + str(last_row_db + 1) + "', '" + str(login) + "', '" + str(
            password) + "', 'False');"
        return registration_user

# SQL запрос на добавление в таблицу BIOMETRY_SAMPLE
def add_sampe_sql(file):
    byometry_sampe_sql = "INSERT INTO \"BIOMETRY_SAMPLE\" " \
                         "(\"ID_BIOMETRY\", \"USER_ID\", \"SAMPLE\")" \
                         " VALUES ('3', '1', " + str((psycopg2.Binary(file))) + ");"
    return byometry_sampe_sql

# SQL запрос на селект семплом из таблицы BIOMETRY_SAMPLE
def select_sample_sql():
    sammpe_select_sql = "SELECT \"SAMPLE\" " \
                        "FROM \"BIOMETRY_SAMPLE\" " \
                        "WHERE \"ID_BIOMETRY\" = '3'"
    return sammpe_select_sql