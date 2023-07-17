import requests
from requests.exceptions import ConnectionError
requests.packages.urllib3.disable_warnings()

def rest_connect(device, container, headers):

      url = f"https://{device}{container}"

      try:
            response = requests.get(
                                    url,
                                    headers=headers,
                                    verify=False,
                                    timeout=3)

            if response.status_code == 200:

                  return response.json(), True

      except ConnectionError:

            return f"ConnectionError", False

      return f"unsuccessful connection", False
