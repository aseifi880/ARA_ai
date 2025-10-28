# python standard libraries
import os

# third-party libraries
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# local application libraries
from repository.jobyabi_repository import JobyabiRepo
from services.jobyabi_service import JobyabiService
from helpers.response_formatter import sanitize

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
            sanitized = sanitize(resumes)
            return Response({"results": sanitized})
        finally:
            repo.close()


class JobyabiJobsView(APIView):
    def get(self, request: Request):
        refresh = request.query_params.get("refresh", "false").lower() == "true"
        limit = int(request.query_params.get("limit", 50))

        repo = JobyabiRepo(MONGO_URI)
        service = JobyabiService(repo)
        try:
            jobs = service.get_jobs(force_refresh=refresh, limit=limit)
            sanitized = sanitize(jobs)
            return Response({"results": sanitized})
        finally:
            repo.close()
