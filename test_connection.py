# test_connection.py
import pyodbc
import os


def test_sql_server():
    print("🔍 Тестируем подключение к SQL Server...")

    server = r'MONSIER\SQLEXPRESS'
    database = 'movie_reviews_db'

    # Строка подключения для Windows Authentication
    conn_str = f'''
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={server};
        DATABASE={database};
        Trusted_Connection=yes;
        TrustServerCertificate=yes;
    '''

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Проверка версии
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"✅ Подключение успешно!")
        print(f"📊 SQL Server: {version.split('\\n')[0]}")

        # Проверка базы данных
        cursor.execute("""
            SELECT name, create_date 
            FROM sys.databases 
            WHERE name = ?
        """, database)
        db_info = cursor.fetchone()

        if db_info:
            print(f"✅ База данных '{db_info[0]}' найдена")
            print(f"📅 Создана: {db_info[1]}")
        else:
            print(f"⚠️ База данных '{database}' не найдена")
            print("Создайте её в SSMS командой: CREATE DATABASE movie_reviews_db;")

        conn.close()
        return True

    except pyodbc.Error as e:
        print(f"❌ Ошибка подключения: {e}")
        return False


if __name__ == '__main__':
    test_sql_server()