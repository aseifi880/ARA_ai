from bs4 import BeautifulSoup

from helpers.cleaners import multiline_to_one, remove_extra_space
from scrapers import JobyabiScraper


class JobyabiResumeScraper(JobyabiScraper):
    resumes_page_endpoint = "/archives/cvs.php"

    @staticmethod
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

    @staticmethod
    def scrape_resume_contents(soup: BeautifulSoup) -> dict[str, dict]:
        """
        Get soup for the resume page. Parse the page for details including :
        applicant's personal info, past job experiences (position, work place, years), abilities,
        education history, language
        :param soup: BeautifulSoup object
        :return: dict[str, str]
        """
        resume = {}
        el_name = soup.find("div", {"class": "cv_name_s"})
        applicant_name = (
            el_name.find(text=True, recursive=False).get_text(strip=True)
            if el_name
            else ""
        )
        applicant_birthdate_marriage = (
            remove_extra_space(el_name.find("span").get_text(strip=True))
            if el_name
            else ""
        )
        resume_right_side = soup.find("div", {"class": "cvv_right"})
        el_location = soup.find("span", {"class": "cvv_location"})
        applicant_location = el_location.get_text(strip=True) if el_location else ""
        resume_left_side = soup.find("div", {"class": "cvv_left"})
        applicant_aboutme = (
            multiline_to_one(
                remove_extra_space(
                    resume_left_side.find("div", {"class": "cvv_aboutme"}).get_text(
                        strip=True
                    )
                )
            )
            if resume_left_side
            else ""
        )

        work_experience = []
        find_work_icon = (
            resume_left_side.find("span", {"class": "cvv_pre_work"})
            if resume_left_side
            else ""
        )
        work_icon_parent = find_work_icon.find_parent("div") if find_work_icon else None
        work_exp_table = (
            work_icon_parent.find_next("table") if work_icon_parent else None
        )
        if work_exp_table is not None:
            for row in work_exp_table.find_all("tr")[1:]:
                col_data = [td.get_text(strip=True) for td in row.find_all("td")]
                if len(col_data) == 3:
                    work_experience.append(
                        {
                            "position": col_data[0],
                            "work place": col_data[1],
                            "curr_status": col_data[2],
                        }
                    )

        edu_history = []
        find_edu_icon = resume_left_side.find("span", {"class": "cvv_edu_ico"})
        parent = find_edu_icon.find_parent("div") if find_edu_icon else None
        education_history_table = parent.find_next("table") if parent else None
        if education_history_table is not None:
            for row in education_history_table.find_all("tr")[1:]:
                col_data = [td.getText(strip=True) for td in row.find_all("td")]
                if len(col_data) == 2:
                    edu_history.append(
                        {
                            "grade_and_major": col_data[0],
                            "location": col_data[1],
                        }
                    )

        software_abilities = []
        find_sw_icon = resume_left_side.find("span", {"class": "cvv_software_ico"})
        find_parent = find_sw_icon.find_parent("div") if find_sw_icon else None
        software_table = find_parent.find_next("table") if find_parent else None
        if software_table is not None:
            for row in software_table.find_all("tr")[1:]:
                col_data = [td.get_text(strip=True) for td in row.find_all("td")]
                if len(col_data) == 2:
                    software_abilities.append(
                        {
                            "software": col_data[0],
                            "familiarity": col_data[1],
                        }
                    )

        languages = []
        find_lang_icon = resume_left_side.find("span", {"class": "cvv_langs_ico"})
        parent = find_lang_icon.find_parent("div") if find_lang_icon else None
        languages_table = parent.find_next("table") if parent else None
        if languages_table is not None:
            for row in languages_table.find_all("tr")[1:]:
                col_data = [td.get_text(strip=True) for td in row.find_all("td")]
                if len(col_data) == 2:
                    languages.append(
                        {"language": col_data[0], "familiarity": col_data[1]}
                    )

        resume["full_name"] = applicant_name
        resume["birthdate_marriage_status"] = applicant_birthdate_marriage
        resume["location"] = applicant_location
        resume["aboutme"] = applicant_aboutme
        resume["pre_work"] = work_experience
        resume["edu_history"] = edu_history
        resume["software_abilities"] = software_abilities
        resume["languages"] = languages
        return {"resume": resume}
