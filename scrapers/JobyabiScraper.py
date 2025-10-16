from abc import ABC

from bs4 import BeautifulSoup

from scrapers import BaseScraper


class JobyabiScraper(BaseScraper, ABC):
    base_url = "https://www.jobyabi.com"

    def scrape_resume_contents(self, soup: BeautifulSoup) -> list:
        pass


def scrape_resume_links(soup: BeautifulSoup) -> list:
    resume_anchor_els = soup.find_all("a", {"class": "cvs_arch_show_link"})
    links = []
    for link in resume_anchor_els:
        links.append(link.get("href"))
    return links
