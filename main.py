from scrapers import JobyabiScraper, scrape_resume_links


def main():
    js = JobyabiScraper()
    print("Fetching main site content ...", end=" ")
    jobyabi_html = js.fetch("/archives/cvs.php")
    print("Fetch Complete.")
    soup = js.get_soup(jobyabi_html)
    links = scrape_resume_links(soup)

    soups = []
    for link in links:
        print("FETCHING DETAIL PAGE ...", end=" ")
        html = js.fetch(link)
        print("Fetch Complete.")
        soup = js.get_soup(html)
        soups.append(soup)

    print(soups)

if __name__ == "__main__":
    main()