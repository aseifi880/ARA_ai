from scrapers import JobyabiScraper, scrape_resume_links


def main():
    js = JobyabiScraper()
    print("Fetching main site content ...", end=" ")
    jobyabi_html = js.fetch("/archives/cvs.php")
    print("Fetch Complete.")
    soup = js.get_soup(jobyabi_html)
    links = scrape_resume_links(soup)


if __name__ == "__main__":
    main()