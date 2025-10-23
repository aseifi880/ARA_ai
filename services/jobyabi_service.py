from typing import List, Dict, Optional
from datetime import timedelta
from scrapers.jobyabi_job_scraper import JobyabiJobScraper
from scrapers.jobyabi_resume_scraper import JobyabiResumeScraper
from repository.jobyabi_repository import JobyabiRepo

DEFAULT_MAX_AGE_SECONDS = 60 * 10  # 10 minutes


class JobyabiService:
    def __init__(self, repo: JobyabiRepo, max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS):
        self.repo = repo
        self.max_age_seconds = max_age_seconds
        self.job_scraper = JobyabiJobScraper()
        self.resume_scraper = JobyabiResumeScraper()

    # ---------------- Jobs ----------------

    # TODO add methods for job service

    # ---------------- Resumes ----------------
    def get_cached_resumes(self, limit: int = 50) -> List[Dict]:
        return self.repo.get_recent_resumes(limit=limit)

    def refresh_resumes(self, page_endpoint: Optional[str] = None, limit_links: Optional[int] = None) -> None:
        # fetch list page:
        endpoint = page_endpoint or self.resume_scraper.resumes_page_endpoint
        html = self.resume_scraper.fetch(endpoint)
        soup = self.resume_scraper.get_soup(html)
        links = self.resume_scraper.scrape_resume_links(soup, limit=limit_links)

        for link in links:
            html_resume = self.resume_scraper.fetch(link)
            soup_resume = self.resume_scraper.get_soup(html_resume)
            content = self.resume_scraper.scrape_resume_contents(soup_resume)
            source_url = self.resume_scraper.request_url or link
            self.repo.upsert_one_resume(source_url=source_url, content=content)

    def get_resumes(self, force_refresh: bool = False, limit: int = 50, limit_links: Optional[int] = None) -> list[dict]:
        if force_refresh:
            self.refresh_resumes(limit_links=limit_links)
            return self.get_cached_resumes(limit=limit)
        recent = self.get_cached_resumes(limit=1)
        if not recent:
            self.refresh_resumes(limit_links=limit_links)
            return self.get_cached_resumes(limit=limit)
        latest = recent[0]
        if self.repo.is_stale(self.repo.resumes, latest["source_url"], self.max_age_seconds):
            self.refresh_resumes(limit_links=limit_links)
        return self.get_cached_resumes(limit=limit)
