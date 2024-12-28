from parser import TransfermarktParser
from translate import Translater
from database.db import PostgreSQLDatabase
import convert_json

if __name__ == "__main__":
    #Инициализируем парсер
    parser = TransfermarktParser()

    # Диапазон ID игроков
    player_ids = range(1, 20)

    # Сбор данных
    players_data = parser.fetch_multiple_players(player_ids)

    #Перевод имен игроков
    translater = Translater()
    players = translater.translate_names(players_data)

    # Сохранение полученных данных в файл json формата
    #convert_json.save_to_json_file(players, "players.json")

    # Сохранение в базу данных PostgreSQL

    db = PostgreSQLDatabase()
    db.connect()
    db.create_table()

    for player in players:
        db.insert_player_data(player)

    db.close()
