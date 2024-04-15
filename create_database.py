import psycopg2


try:
    connection = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='83436891'
    )
    cursor = connection.cursor()
    connection.autocommit = True

    create_db = 'CREATE DATABASE headhunter'
    cursor.execute(create_db)
    cursor.close()
    connection.close()
except:
    print('База данных уже создана.')
