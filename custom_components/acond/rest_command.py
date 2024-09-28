POST_ACOND_URL = "http://10.0.1.105/PAGE115.xml"
USERNAME = "acond"
PASSWORD = "acond"

def post_acond_temperature(hass, temperature):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = f"__TB48CC351_REAL_.1f={temperature}"

    response = requests.post(POST_ACOND_URL, auth=(USERNAME, PASSWORD), headers=headers, data=payload)
    if response.status_code != 200:
        hass.logger.error("Failed to post Acond temperature")
