# third-party libraries
from rest_framework.views import APIView

# local application libraries
from scrapers import jobyabi_resume_scraper, jobyabi_job_scraper


# Create your views here.
class JobyabiJobView(APIView):
    def get(self, request, *args, **kwargs):
        pass
