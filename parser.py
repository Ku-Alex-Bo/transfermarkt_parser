import requests
import re
from bs4 import BeautifulSoup

class TransfermarktParser:
    """Класс для парсинга игроков с сайта Transfermarkt."""

    BASE_URL = "https://www.transfermarkt.com/a/profil/spieler/"

    def __init__(self, headers=None) -> None:
        """Инициализация сессии и заголовков."""
        self.session = requests.Session()
        self.session.headers.update(headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        })

    def get_player_data(self, player_id) -> dict:
        """Получить данные об игроке по ID."""
        url = f"{self.BASE_URL}{player_id}"
        try:
            response = self.session.get(url)
            if response.status_code != 200:
                return {"ID": player_id, "Error": "Page not found"}

            soup = BeautifulSoup(response.content, "html.parser")

            name = self.get_name(url=response.url)
            shirt_number = self.get_shirt_number(soup=soup)
            full_name = self.get_full_name(soup)
            birth_date = self.get_birth_date(soup)
            national = self.get_national(soup)
            position = self.get_main_position(soup)
            current_club = self.get_current_club(soup)

            return {
                "player_id": player_id,
                "name": name,
                "shirt_number": shirt_number,
                "full_name": full_name,
                "birth_date": re.sub(r'\(\d+\)', '', birth_date).strip() if birth_date else None,
                "national": national,
                "position": position,
                "current_club": current_club
            }

        except requests.RequestException as e:
            return {"ID": player_id, "Error": f"Request failed: {e}"}

    @staticmethod
    def get_name(url: str) -> str:
        """Извлечение имени из URL."""
        try:
            name_match = re.search(string=url, pattern=r"(?<=\.com/)[a-z-]+(?=/)")
            name = name_match.group().replace("-", " ") if name_match else None
            return name
        except Exception as e:
            print(f"Ошибка извлечения имени: {e}")
            return None

    @staticmethod
    def get_shirt_number(soup: BeautifulSoup) -> str:
        """Извлечение номера игрока."""
        try:
            shirt_number_soup = soup.find("span", class_="data-header__shirt-number")
            shirt_number = shirt_number_soup.text.strip().replace("#", "№") if shirt_number_soup else None
            return shirt_number
        except Exception as e:
            print(f"Ошибка извлечения номера: {e}")
            return None

    def get_data(func):
        """Декоратор в который передаем фукнции для извлечения необходимых данных из блока"""
        def wrapper(self, soup: BeautifulSoup):
            try:
                data_soup = soup.find("div", class_=re.compile(r'info-table info-table--right-space'))
                element = func(self, data_soup)
                return element.text.strip()
            except:
                return None
        return wrapper

    @get_data
    def get_full_name(self, data_soup):
        """Получить полное имя игрока."""
        return data_soup.find(
            'span',
            string=lambda s: s and ('Name in home country:' in s or 'Full name:' in s)
        ).find_next('span', class_='info-table__content--bold')

    @get_data
    def get_birth_date(self, data_soup):
        """Получить дату рождения игрока"""
        return data_soup.find(
            'span',
            string=lambda s: s and "Date of birth/Age:" in s
        ).find_next('span', class_='info-table__content--bold')

    @get_data
    def get_national(self, data_soup):
        """Получить национальность игрока"""
        return data_soup.find(
            'span',
            string=lambda s: s and "Citizenship:" in s
        ).find_next('span', class_='info-table__content--bold')

    @get_data
    def get_main_position(self, data_soup):
        """Получить основную позицию игрока"""
        return data_soup.find(
            'span',
            string=lambda s: s and "Position:" in s
        ).find_next('span', class_='info-table__content--bold')

    @get_data
    def get_current_club(self, data_soup):
        """Получить текущий клуб игрока"""
        return data_soup.find(
            'span',
            string=lambda s: s and "Current club:" in s
        ).find_next('span', class_='info-table__content--bold')

    def fetch_multiple_players(self, player_ids):
        """Получить данные для нескольких игроков."""
        return [self.get_player_data(player_id) for player_id in player_ids]
