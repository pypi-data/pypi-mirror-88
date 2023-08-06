# *-* coding:utf-8 *-*

from .sca_tork_easycube_api_helpers import SCATorkEasyCubeAPIHelpers
import requests
import pandas as pd
from altf1be_helpers import AltF1BeHelpers, AltF1BeJSONHelpers
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import json
import logging
import os

import sys
sys.path.append(os.path.join(os.getcwd()))
# 'dispensers_model.py.log'
log_filename = AltF1BeHelpers.create_append_log_file(
    f"{os.path.basename(__file__)}.log"
)
logger = AltF1BeHelpers.get_logger(
    log_level=logging.INFO,
    # log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_filename=log_filename
)

credentials_filename = os.path.join(
    "credentials", "sca_tork_easycube_api_credentials.json")


class SCATorkEasyCubeAPIAuthentication(SCATorkEasyCubeAPIHelpers):
    """
        Collect data about dispensers from SCA Tork Easycube API

        See Swagger for Developers: https://easycube-external-api-web-c2m2jq5zkw6rc.azurewebsites.net/swagger
    """
    is_connected = False

    def __authentication(self):
        self.is_connected = False
        logger.info(
            f"START : sca_tork_easycube_api_authentication"
        )

        client_id = os.environ.get("SCA_TORK_EASYCUBE_CLIENT_ID", None)
        client_secret = os.environ.get("SCA_TORK_EASYCUBE_CLIENT_SECRET", None)
        grant_type = os.environ.get("SCA_TORK_EASYCUBE_GRANT_TYPE", None)
        scope = os.environ.get("SCA_TORK_EASYCUBE_SCOPE", None)

        stop = False
        if client_id is None:
            logger.info("ERROR: client_id env variable is missing")
            logger.info("run source ~/.profile")
            stop = True

        if client_secret is None:
            logger.info("ERROR: client_secret env variable is missing")
            logger.info("run source ~/.profile")
            stop = True

        if grant_type is None:
            logger.info("ERROR: grant_type env variable is missing")
            logger.info("run source ~/.profile")
            stop = True

        if scope is None:
            logger.info("ERROR: scope env variable is missing")
            logger.info("run source ~/.profile")
            stop = True

        if stop == True:
            exit()

        url = "https://login.easycube.torkglobal.com/connect/token"

        payload = f'client_id={client_id}&client_secret={client_secret}&grant_type={grant_type}&scope={scope}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            response = requests.request(
                "POST", url, headers=headers, data=payload)

            data = response.text.encode(
                'utf8'
            )
            self.authorization = f'Bearer {json.loads(data)["access_token"]}'
            # response.text.encode('utf8')

            # store credentials on the disk

            AltF1BeJSONHelpers().save(
                data=data,
                filename=credentials_filename
            )
            self.is_connected = True

        except requests.exceptions.ConnectionError as e:
            self.is_connected = False
            logger.exception(e)

    def __init__(self):
        super().__init__()
        self.__authentication()


if __name__ == "__main__":
    sCATorkEasyCubeAPIAuthentication = SCATorkEasyCubeAPIAuthentication()
    logger.info(
        f"sCATorkEasyCubeAPIAuthentication.is_connected: {sCATorkEasyCubeAPIAuthentication.is_connected}"
    )
