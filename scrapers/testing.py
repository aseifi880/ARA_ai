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


# use to test jobyabi link scraping
def main():
    jjs = JobyabiJobScraper()
    today_jobs = jjs.fetch(jjs.today_job_posting_endpoint)
    soup = jjs.get_soup(today_jobs)
    links = jjs.scrape_job_links_for_today(soup)
    print(links)
    for link in links:
        html = jjs.fetch(link)
        soup = jjs.get_soup(html)
        pprint(jjs.scrape_job_content_from_job_page(soup))


if __name__ == "__main__":
    main()
