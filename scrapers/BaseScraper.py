from abc import ABC
import httpx
from bs4 import BeautifulSoup


class BaseScraper(ABC):
    """
    Define base class for all scrapers.
    Construction takes site_url as only input.
    Based on site fetch and parse methods can be overwritten.
    """

    headers = {"User-Agent": "Mozilla/5.0"}

    base_url: str = ""
    request_url: str = ""

    def __init__(self, base_url=None):
        if self.base_url == "" and base_url is not None:
            self.base_url = base_url

    def fetch(self, endpoint: str = "") -> str:
        """
        Get content of base_url + endpoint, and return it as a string.
        :param endpoint: str
        """
        req_url = f"{self.base_url}{endpoint}"
        self.request_url = f"{self.base_url}{endpoint}"
        res = httpx.get(req_url, headers=self.headers)
        res.raise_for_status()
        return res.text

    @staticmethod
    def get_soup(html: str) -> BeautifulSoup:
        """
        Return BeautifulSoup object from html string.
        :param html: str
        :return: BeautifulSoup
        """
        return BeautifulSoup(html, "lxml")
