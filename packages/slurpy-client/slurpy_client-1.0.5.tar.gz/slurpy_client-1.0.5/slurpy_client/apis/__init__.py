
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.email_api import EmailApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from slurpy_client.api.email_api import EmailApi
from slurpy_client.api.inbox_api import InboxApi
from slurpy_client.api.jobs_api import JobsApi
