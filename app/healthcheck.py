import sys
import urllib.request
from http.client import HTTPResponse

# Healthcheck: Attempting to send an HTTP request to the backend
try:
    response: HTTPResponse = urllib.request.urlopen('http://localhost:8000/health')  # Accessing backend URL
    if response.status == 200:  # If the response is successful (200 OK)
        sys.exit(0)  # Successful healthcheck (exit code 0)
    else:
        sys.exit(1)  # If the response is not 200, healthcheck fails (exit code 1)
except Exception:  # Catching any exception (like connection errors)
    sys.exit(1)  # If an error occurs (e.g., backend is unreachable), healthcheck fails (exit code 1)
