from typing import Any

from bs4 import BeautifulSoup

from helpers.cleaners import get_url_path_with_params
from scrapers import JobyabiScraper


class JobyabiJobScraper(JobyabiScraper):

    # use below links as class instance attributes to use inside fetch method
    # jjs.recent_job_posting_endpoint
    recent_job_postings_endpoint = "/"

    @property
    def today_job_posting_endpoint(self):
        return "/topics/استخدام-های-امروز"
    @staticmethod
    def scrape_job_links_for_today(soup: BeautifulSoup, limit: int = None) -> list[str]:
        job_postings = soup.find_all("div", {"class": "n_cell"})
        anchor_els = [job_posting.find("a") for job_posting in job_postings]
        links = [get_url_path_with_params(link.get("href")) for link in anchor_els]
        return links

    @staticmethod
    def scrape_recent_jobs_links(soup: BeautifulSoup, limit: int = 10) -> list[str]:
        """
        get soup for the page recent_job_postings_endpoint, return list of links in string
        :param soup: BeautifulSoup object
        :param limit: int, default 10
        :return:
        """
        job_postings_list = soup.find("ul", {"class": "list_item2"})
        job_anchor_els = job_postings_list.find_all("a")
        job_links = [a.get("href") for a in job_anchor_els]
        return job_links

    @staticmethod
    def scrape_job_content_from_job_page(soup: BeautifulSoup) -> dict[str, Any]:
        """
        Get soup for the job description page and return a dict of key values concerning the job details
        :param soup: BeautifulSoup object
        :return: returns a dict
        """
        content = {}
        page_title = soup.find("h2", {"class": "n_page_title"}).get_text()
        content["page_title"] = page_title

        job_titles_h3 = soup.find_all("h3")[:-3]
        job_titles = [job_title.get_text(strip=True) for job_title in job_titles_h3]
        content["job_titles"] = job_titles

        job_info_paragraphs = soup.find("div", {"class": "n_cell"}).find_all("p")
        content["job_info"] = [p.get_text(strip=True) for p in job_info_paragraphs]

        content["job_location"] = (soup.find("span", {"class": "post_pos_sim"})
                                   .find_next_sibling("a")
                                   .get_text(strip=True))

        content["salary"] = soup.find("span", {"class": "post_sal_sim"}).parent.get_text(strip=True)

        content["required_education"] = (soup.find("span", {"class": "post_edu_sim"})
                                         .parent.get_text(strip=True))
        return content
