from googletrans import Translator
from typing import List

class Translater:
    def translate_names(self, players: List[dict]) -> List[dict]:
        for player in players:
            player["ru_name"] =  self.get_translate(player["name"]) if player["name"] else None
            player["ru_full_name"] =  self.get_translate(player["full_name"]) if player["full_name"] else None

        return players

    @staticmethod
    def get_translate(ru_string: str) -> str:
        translator = Translator()
        translated = translator.translate(ru_string, src="auto", dest="ru").text
        return translated
