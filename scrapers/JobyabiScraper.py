#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard libraries
from abc import ABC

# related third-party libraries
from bs4 import BeautifulSoup

# local-application libraries
from scrapers import BaseScraper
from helpers.cleaners import remove_extra_space

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
    applicant_name = soup.find("div", {"class": "cv_name_s"}).find(text=True, recursive=False).get_text(strip=True)
    applicant_birthdate_marriage = remove_extra_space(soup.find("div", {"class": "cv_name_s"}).find("span").get_text(strip=True))
    resume_right_side = soup.find("div", {"class": "cvv_right"})
    applicant_location = soup.find("span", {"class": "cvv_location"}).get_text(strip=True)
    resume_left_side = soup.find("div", {"class": "cvv_left"})
    applicant_aboutme = resume_left_side.find("div", {"class": "cvv_aboutme"}).get_text(strip=True)

    work_experience = []
    work_exp_table = resume_left_side.find("span", {"class": "cvv_pre_work"}).find_parent("div").find_next("table")
    for row in work_exp_table.find_all("tr")[1:]:
        col_data = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(col_data) == 3:
            work_experience.append({
                "position": col_data[0],
                "work place": col_data[1],
                "curr_status": col_data[2],
            })

    edu_history = []
    education_history_table = (resume_left_side
                               .find("span", {"class": "cvv_edu_ico"})
                               .find_parent("div")
                               .find_next("table"))
    for row in education_history_table.find_all("tr")[1:]:
        col_data = [td.getText(strip=True) for td in row.find_all("td")]
        if len(col_data) == 2:
            edu_history.append({
                "grade_and_major": col_data[0],
                "location": col_data[1],
            })

    software_abilities = []
    software_table = resume_left_side.find("span", {"class": "cvv_software_ico"}).find_parent("div").find_next("table")
    for row in software_table.find_all("tr")[1:]:
        col_data = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(col_data) == 2:
            software_abilities.append({
                "software": col_data[0],
                "familiarity": col_data[1],
            })

    languages = []
    languages_table = resume_left_side.find("span", {"class": "cvv_langs_ico"}).find_parent("div").find_next("table")
    for row in languages_table.find_all("tr")[1:]:
        col_data = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(col_data) == 2:
            languages.append({
                "language": col_data[0],
                "familiarity": col_data[1]
            })

    resume["full_name"] = applicant_name
    resume["birthdate_marriage_status"] = applicant_birthdate_marriage
    resume["location"] = applicant_location
    resume["aboutme"] = applicant_aboutme
    resume["pre_work"] = work_experience
    resume["edu_history"] = edu_history
    resume["software_abilities"] = software_abilities
    resume["languages"] = languages
    return {"resume": resume}


def scrape_resume_links(soup: BeautifulSoup, limit: int = None) -> list[str]:
    """
    Receive soup for a page of Jobyabi.com/archives/cvs.php?<Page queries>
    Return the endpoints for all the resume listings in that page if no limit given.
    :param limit: int
    :param soup: BeautifulSoup
    :return: list[str]
    """
    resume_anchor_els = soup.find_all("a", {"class": "cvs_arch_show_link"})
    if limit:
        resume_anchor_els = resume_anchor_els[:limit]
    links = []
    for link in resume_anchor_els:
        links.append(link.get("href"))
    return links


