import psycopg2
from psycopg2 import sql

from dotenv import load_dotenv
import os

class PostgreSQLDatabase:
    """Класс для работы с PostgreSQL."""

    def __init__(self):
        """Инициализация подключения к базе данных с использованием dotenv."""
        load_dotenv()
        self.db_config = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
        }
        self.connection = None

    def connect(self):
        """Установить соединение с базой данных."""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            print("Соединение с базой данных успешно установлено.")
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def close(self):
        """Закрыть соединение с базой данных."""
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто.")

    def create_table(self):
        """Создать таблицу для хранения данных игроков, если она не существует."""
        query = """
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY,
            name VARCHAR(255),
            ru_name VARCHAR(255),
            full_name VARCHAR(255),
            ru_full_name VARCHAR(255),
            shirt_number VARCHAR(3),
            birth_date VARCHAR(30),
            national VARCHAR(255),
            position VARCHAR(255),
            current_club VARCHAR(255)
        );
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
                print("Таблица 'players' успешно создана (или уже существует).")
        except psycopg2.Error as e:
            print(f"Ошибка при создании таблицы: {e}")

    def insert_player_data(self, player: dict):
        """Вставить данные игрока в таблицу."""
        query = """
        INSERT INTO players (player_id, name, ru_name, full_name, ru_full_name, shirt_number, birth_date, national, position, current_club)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (player_id) DO NOTHING;
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (
                    player["player_id"],
                    player["name"],
                    player["ru_name"],
                    player["full_name"],
                    player["ru_full_name"],
                    player["shirt_number"],
                    player["birth_date"],
                    player["national"],
                    player["position"],
                    player["current_club"]
                ))
                self.connection.commit()
                print(f"Данные игрока {player['name']} успешно добавлены.")
        except psycopg2.Error as e:
            print(f"Ошибка при вставке данных: {e}")
