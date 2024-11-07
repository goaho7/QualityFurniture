import requests
from urllib3 import Retry


REQUESTS_SESSION = requests.Session()
REQUESTS_ADAPTER = requests.adapters.HTTPAdapter(
    pool_connections=100,
    pool_maxsize=100,
    max_retries=Retry(
        total=3,
        connect=3,
        backoff_factor=3,
        backoff_max=25,
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_redirect=False,
    ),
)
REQUESTS_SESSION.mount("http://", REQUESTS_ADAPTER)