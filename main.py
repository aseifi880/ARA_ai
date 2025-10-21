# standard libraries
from pprint import pprint

# third-party libraries
from bs4 import BeautifulSoup

# local-application libraries
from scrapers import JobyabiResumeScraper, JobyabiJobScraper
from html_text import text


# use for testing resume scraping  with local html files
# def main():
#     soup = BeautifulSoup(text, "html.parser")
#     resume = scrape_resume_contents(soup)
#     pprint(resume)


# use to test resume fetch request
# def main():
#     jrs = JobyabiResumeScraper()
#     print("Fetching main site content...", end=" ")
#     jobyabi_html = jrs.fetch(jrs.resumes_page_endpoint)
#     print("Fetch Complete.")
#     print("Finding resume links in main page...", end=" ")
#     soup = jrs.get_soup(jobyabi_html)
#     links = jrs.scrape_resume_links(soup, limit=1)
#     print("Done.")
#     for link in links:
#         print("Fetching resume link content...")
#         resume_html = jrs.fetch(link)
#         print("Fetch Complete.")
#         resume_soup = jrs.get_soup(resume_html)
#         pprint(jrs.scrape_resume_contents(resume_soup))


# use to test jobyabi job scraping
def main():
    jjs = JobyabiJobScraper()
    recent_jobs_html = jjs.fetch(jjs.recent_job_postings_endpoint)
    soup = jjs.get_soup(recent_jobs_html)
    links = jjs.scrape_recent_jobs_links(soup)
    print(links)


if __name__ == "__main__":
    main()
