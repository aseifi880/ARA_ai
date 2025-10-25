# python standard libraries
import os

# third-party libraries
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# local application libraries
from repository.jobyabi_repository import JobyabiRepo
from services.jobyabi_service import JobyabiService

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")


# Create your views here.
class JobyabiResumeView(APIView):
    def get(self, request: Request):
        refresh = request.query_params.get("refresh", "false").lower() == "true"
        limit = int(request.query_params.get("limit", 50))

        repo = JobyabiRepo(MONGO_URI)
        service = JobyabiService(repo)
        try:
            resumes = service.get_resumes(force_refresh=refresh, limit=limit)
            # jobs are raw DB docs; convert to JSON friendly dicts
            # remove ObjectId if present, convert datetime to iso format
            sanitized = []
            for r in resumes:
                content = r.get("content", {})
                src = r.get("source_url")
                fetched_at = r.get("fetched_at")
                fetched_at_iso = fetched_at.isoformat() if fetched_at else None
                sanitized.append({"source_url": src, "fetched_at": fetched_at_iso, "content": content})
            return Response({"results": sanitized})
        finally:
            repo.close()
