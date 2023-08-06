# *-* coding:utf-8 *-*

from .sca_tork_easycube_api_authentication import SCATorkEasyCubeAPIAuthentication
import sys
from altf1be_helpers import AltF1BeHelpers
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

sys.path.append(os.path.join(os.getcwd()))
credentials_filename = os.path.join(
    "credentials", "sca_tork_easycube_api_credentials.json")


class SCATorkEasyCubeAPI(SCATorkEasyCubeAPIAuthentication):
    """
        Collect data about dispensers from SCA Tork Easycube API

        See Swagger for Developers: https://easycube-external-api-web-c2m2jq5zkw6rc.azurewebsites.net/swagger
    """

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    sCATorkEasyCubeAPI = SCATorkEasyCubeAPI()
    logger.info(
        f'sCATorkEasyCubeAPI.is_connected: {sCATorkEasyCubeAPI.is_connected}'
    )
    if sCATorkEasyCubeAPI.is_connected == True:
        sCATorkEasyCubeAPI.save_api_data()
