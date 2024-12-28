import json

def save_to_json_file(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в файл {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении в файл: {e}")
