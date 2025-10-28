from datetime import datetime, timezone
from typing import Iterable, Any

from pymongo import MongoClient, ASCENDING, UpdateOne
from pymongo.collection import Collection


class JobyabiRepo:

    def __init__(self, mongo_url: str):
        """
        jobyabi repo class requires the url of a mongodb for initialization
        :param mongo_url: str
        """
        self.client = MongoClient(mongo_url)
        self.db = self.client['scraped_db']
        self.jobs: Collection = self.db['jobs']
        self.resumes: Collection = self.db['resumes']

        self.jobs.create_index([("source_url", ASCENDING)], unique=True)
        self.resumes.create_index([("source_url", ASCENDING)], unique=True)

        self.jobs.create_index([("fetched_at", ASCENDING)])
        self.resumes.create_index([("fetched_at", ASCENDING)])

    # region resume_methods
    def upsert_one_resume(self, source_url: str, content: dict[str, str | dict]) -> None:
        """
        source_url:
        """
        doc: dict[str, str] = {
            "source_url": source_url,
            "content": content,
            "fetched_at": datetime.now()
        }
        self.resumes.update_one({"source_url": source_url}, {"$set": doc}, upsert=True)

    def bulk_upsert_resumes(self, items: Iterable[dict[str, Any]]) -> None:
        """
        items should be iterable of {"source_url": str, "content": dict}
        Bulk upsert for efficiency.
        """
        ops = []
        for item in items:
            src = item["source_url"]
            doc = {"source_url": src, "content": item["content"], "fetched_at": datetime.now()}
            ops.append(
                {"update_one": {"filter": {"source_url": src}, "update": {"$set": doc}, "upsert": True}}
            )
        if ops:
            self.resumes.bulk_write(
                [UpdateOne(op["update_one"]["filter"], op["update_one"]["update"], upsert=True)
                 for op in ops])

    def get_recent_resumes(self, limit: int = 0) -> list[dict[str, Any]]:
        """
        gets all the resumes, sorts by the time of fetching and displays limited number of them
        :param limit: number of resumes to display
        """
        return list(self.resumes.find().sort("fetched_at", -1).limit(limit))

    # endregion

    # region job_methods
    def upsert_one_job(self, source_url: str, content: dict[str, str]) -> None:
        doc: dict[str, str] = {
            "source_url": source_url,
            "content": content,
            "fetched_at": datetime.now()
        }
        self.jobs.update_one({"source_url": source_url}, {"$set": doc}, upsert=True)

    def bulk_upsert_jobs(self, items: Iterable[dict[str, Any]]) -> None:
        ops = []
        for item in items:
            src = item["source_url"]
            doc: dict[str, str] = {
                "source_url": src,
                "content": item["content"],
                "fetched_at": datetime.now()
            }
            ops.append({
                "update_one": {
                    "filter": {"source_url": src},
                    "update": {"$set": doc},
                    "upsert": True
                }
            })
        if ops:
            # bulk_write requires an iterable of the operations to be sent to server
            # as code is in test phase some cluttering is present in my code, sorry
            self.jobs.bulk_write([
                UpdateOne(op["update_one"]["filter"], op["update_one"]["update"], upsert=True)
                for op in ops])

    def get_recent_jobs(self, limit=0) -> list[dict[str, Any]]:
        """
        gets recent jobs, order by fetch time display by limit if given
        """
        return list(self.jobs.find().sort("fetched_at", -1).limit(limit))

    # endregion

    @staticmethod
    def is_stale(collection: Collection, source_url: str, max_age_seconds: int) -> bool:
        """
        Return True if document does not exist or was fetched earlier than max_age_seconds ago.
        """
        doc = collection.find_one({"source_url": source_url}, {"fetched_at": 1})
        if not doc or "fetched_at" not in doc:
            return True
        fetched_at = doc["fetched_at"]
        age = (datetime.now() - fetched_at)
        return age.total_seconds() > max_age_seconds

    def close(self):
        self.client.close()
