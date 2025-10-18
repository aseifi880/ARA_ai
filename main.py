# standard libraries
from pprint import pprint

# third-party libraries
from bs4 import BeautifulSoup

# local-application libraries
from scrapers import JobyabiScraper, scrape_resume_links, scrape_resume_contents
from html_text import text


# use for testing with local html files
# def main():
#     soup = BeautifulSoup(text, "html.parser")
#     resume = scrape_resume_contents(soup)
#     pprint(resume)


# use to test fetch request
def main():
    js = JobyabiScraper()
    print("Fetching main site content...", end=" ")
    jobyabi_html = js.fetch("/archives/cvs.php")
    print("Fetch Complete.")
    print("Finding resume links in main page...", end=" ")
    soup = js.get_soup(jobyabi_html)
    links = scrape_resume_links(soup, limit=1)
    print("Done.")
    for link in links:
        print("Fetching resume link content...")
        resume_html = js.fetch(link)
        print("Fetch Complete.")
        resume_soup = js.get_soup(resume_html)
        pprint(scrape_resume_contents(resume_soup))


if __name__ == "__main__":
    main()
