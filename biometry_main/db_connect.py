import psycopg2
import critical_info as ci


# коннект к бд и исполнение запросов, автоматический дисконнект также тут
# в select передается текстовое поле "select" если выборка из бд в ином случае ""
def connect_db(sql, select):
    connection_db = psycopg2.connect(
        database=ci.bd_name,
        user=ci.login,
        password=ci.password,
        host=ci.server,
        port=ci.port
    )
    cursor = connection_db.cursor()
    cursor.execute(sql)
    connection_db.commit()
    if select == "select_sample":
        result = bytes(cursor.fetchone()[0])
        return result
    if select == "select":
        result = cursor.fetchall()
        cursor.close()
        connection_db.close()
        return result
    cursor.close()
    connection_db.close()
