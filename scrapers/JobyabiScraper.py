from abc import ABC

from bs4 import BeautifulSoup

from scrapers import BaseScraper


class JobyabiScraper(BaseScraper, ABC):
    base_url = "https://www.jobyabi.com"


def scrape_resume_contents(soup: BeautifulSoup) -> dict[str, dict]:
    """
    Get soup for the resume page. Parse the page for details including :
    applicant's personal info, past job experiences (position, work place, years), abilities,
    education history, language
    :param soup: BeautifulSoup object
    :return: dict[str, str]
    """
    resume = {}
    resume_applicant_pi = soup.find("div", {"class": "cv_name_s"})
    applicant_name = resume_applicant_pi.text
    applicant_birthdate_marriage = resume_applicant_pi.find("span").text
    resume_right_side = soup.find("div", {"class": "cvv_right"})
    applicant_location = soup.find("div", {"class": "cvv_location"})
    resume_left_side = soup.find("div", {"class": "cvv_left"})
    applicant_aboutme = resume_left_side.find("div", {"class": "cvv_aboutme"})

    work_experience = []
    work_exp_table = resume_left_side.find("span", {"class": "cvv_pre_work"}).find_parent("div").find_next("table")
    for tr in work_exp_table.find_all("tr")[1:]:
        col_data = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(col_data) == 3:
            work_experience.append({
                "position": col_data[0],
                "work place": col_data[1],
                "curr_status": col_data[2],
            })



    resume["applicant_name"] = applicant_name
    resume["applicant_birthdate_and_marriage"] = applicant_birthdate_marriage
    resume["applicant_location"] = applicant_location
    resume["applicant_aboutme"] = applicant_aboutme
    resume["work_experience"] = work_experience
    return {"resume": resume}


def scrape_resume_links(soup: BeautifulSoup) -> list[str]:
    """
    Receive soup for a page of Jobyabi.com/archives/cvs.php?<Page queries>
    Return the endpoints for all the resume listings in that page.
    :param soup:
    :return:
    """
    resume_anchor_els = soup.find_all("a", {"class": "cvs_arch_show_link"})
    links = []
    for link in resume_anchor_els:
        links.append(link.get("href"))
    return links


