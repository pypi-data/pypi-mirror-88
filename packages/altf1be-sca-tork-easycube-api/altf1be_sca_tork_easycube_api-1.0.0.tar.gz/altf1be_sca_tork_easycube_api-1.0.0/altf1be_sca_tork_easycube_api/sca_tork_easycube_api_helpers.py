# *-* coding:utf-8 *-*

import requests
import pandas as pd
from dotenv import load_dotenv
from altf1be_helpers import AltF1BeHelpers, AltF1BeJSONHelpers
import json
import logging
import os

import sys
sys.path.append(os.path.join(os.getcwd()))

# filename_log = 'sca_tork_easycube_api_helpers.py.log'
log_filename = AltF1BeHelpers.create_append_log_file(
    f"{os.path.basename(__file__)}.log"
)

logger = AltF1BeHelpers.get_logger(
    log_level=logging.INFO,
    # log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_filename=log_filename
)


credentials_filename = os.path.join(
    "credentials", "sca_tork_easycube_api_credentials.json"
)


class SCATorkEasyCubeAPIHelpers():
    """
    Helpers for SCA Tork Easycube API

    - GET and POST requests to the endpoints

    See Swagger for Developers: https://easycube-external-api-web-c2m2jq5zkw6rc.azurewebsites.net/swagger
    """

    def __set_env_variables(self):
        load_dotenv()
        AltF1BeHelpers.test_environ(["SCA_TORK_EASYCUBE_BASE_URL"])

    def __init__(self):
        self.altF1BeJSONHelpers = AltF1BeJSONHelpers()
        self.__set_env_variables()

    def __del__(self):
        del self.altF1BeJSONHelpers

    def __scramble_data(self, data_str: str):
        data_str = data_str.replace(b"Microsoft", b"FM Tech")
        data_str = data_str.replace(b"Schiphol", b"Antwerpen")
        data_str = data_str.replace(b"Zaventem", b"Paris")
        data_str = data_str.replace(
            b"CEC", b"Headquarter"
        )  # Customer Experience Center
        data_str = data_str.replace(b"A1", b"Prometheus room")
        data_str = data_str.replace(b"A2", b"Athena room")
        data_str = data_str.replace(b"A3", b"Zeus room")
        data_str = data_str.replace(b"Client", b"Guest room")
        data_str = data_str.replace(b"Sodexo", b"Facility operations")
        data_str = data_str.replace(b"14300", b"00000")
        data_str = data_str.replace(b"14301", b"00001")
        data_str = data_str.replace(b"14320", b"00020")
        data_str = data_str.replace(b"14339", b"00039")
        data_str = data_str.replace(b"14351", b"00051")
        data_str = data_str.replace(b"A-03-30-05", b"F-01-05-30")
        data_str = data_str.replace(b"A-04-30-05", b"F-02-05-30")
        data_str = data_str.replace(b"A-04-30-01", b"F-02-01-30")
        return data_str

    def __access_api(self, name, endpoint, output_filename):

        logger.info(
            f"Call SCA Tork API: {name}, {endpoint}, {output_filename}")
        credentials_json = self.altF1BeJSONHelpers.load(
            filename=credentials_filename)

        endpoint = endpoint
        baseUrl = os.environ.get("SCA_TORK_EASYCUBE_BASE_URL")
        if baseUrl is None:
            logger.info(
                "ERROR: SCA_TORK_EASYCUBE_BASE_URL env variable is missing")
            logger.info("run source ~/.profile")
            exit()

        url = f"{baseUrl}{endpoint}"
        # logger.info(f"url: {url}")
        authorization = f'Bearer {credentials_json["access_token"]}'
        # logger.info(f"authorization: {authorization}")
        payload = {}
        headers = {"Authorization": authorization}

        try:
            response = requests.request(
                "GET", url, headers=headers, data=payload)
        except Exception as e:
            logger.exception(e)
            logger.error(f"The {__name__} ended unexpectedtly")
            exit()

        if response.status_code != 200:
            logger.info(f"ERROR: {response.status_code} - {response.reason}")
            logger.info(
                f"run python src-tools/sca-tork-easycube-authentication.py")
            exit()

        # logger.info(response.text.encode('utf8'))
        logger.info(f"{name}, {endpoint}, {output_filename}")
        logger.info(f'{os.path.join("data","api",output_filename)}')

        # TODO: remove the replace of text : Microsoft Schiphol -> FM Tech Antwerpen
        data_str = response.text.encode("utf8")

        data_str = self.__scramble_data(data_str)

        data_str = data_str.decode("utf-8")
        self.altF1BeJSONHelpers.save_with_datetime(
            data=json.dumps(data_str),
            filename=os.path.join(
                "data", "api", "sca-tork-easycube", output_filename),
        )

    def save_api_data(self):
        """store the current data available in the SCA Tork Easycube database

        See https://easycube-external-api-web-c2m2jq5zkw6rc.azurewebsites.net/swagger/index.html
        """

        self.__access_api(
            name="sca_tork_easycube_api_site_peoplecounters_getpresence",
            endpoint="/api/site/PeopleCounters/api/site/PeopleCounters/GetPresence",
            output_filename="sca-tork-easycube-peoplecounters-getpresence.json",
        )

        self.__access_api(
            name="sca_tork_easycube_api_peoplecounters",
            endpoint="/api/site/PeopleCounters",
            output_filename="sca-tork-easycube-peoplecounters.json",
        )

        self.__access_api(
            name="sca_tork_easycube_api_site_dispensers",
            endpoint="/api/site/Dispensers",
            output_filename="sca-tork-easycube-dispensers.json",
        )

        self.__access_api(
            name="sca_tork_easycube_api_locations",
            endpoint="/api/site/Locations",
            output_filename="sca-tork-easycube-locations.json",
        )

        self.__access_api(
            name="sca_tork_easycube_api_site",
            endpoint="/api/Site",
            output_filename="sca-tork-easycube-site.json",
        )

        logger.info(f"END of the collection of SCA Tork Easycube API data")

    def get_api_data(self, endpoint):
        logger.info(f"Get API Data for {endpoint}")

        protocol = "https://"
        base_url = os.environ.get("SCA_TORK_EASYCUBE_BASE_URL")

        url_to_call = f"{base_url}{endpoint}"

        if self.is_connected == False:
            return "{}"

        headers = {"Authorization": self.authorization}

        res = AltF1BeHelpers.requests_retry_session().get(url_to_call, headers=headers)
        logger.info(
            f"http status: {res.status_code} for {AltF1BeHelpers.hide_secrets_from_url(url_to_call)}"
        )

        data = res.content
        data_str = data.decode("utf-8")
        # logger.info(f"API result: {result}")
        # TODO: remove the replace of text : Microsoft Schiphol -> FM Tech Antwerpen

        data_str = self.__scramble_data(data_str)
        return data_str


if __name__ == "__main__":
    sCATorkEasyCubeAPI = SCATorkEasyCubeAPIHelpers()
    sCATorkEasyCubeAPI.save_api_data()
