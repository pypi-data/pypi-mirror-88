# *-* coding:utf-8 *-*

import json
import os
from altf1be_helpers import AltF1BeHelpers
import sys
import logging
log_filename = AltF1BeHelpers.create_append_log_file(
    f"{os.path.basename(__file__)}.log"
)
logger = AltF1BeHelpers.get_logger(
    log_level=logging.INFO,
    # log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_filename=log_filename
)

DISPENSER_TYPE_NOT_FOUND = 'ERROR_DISPENSER_TYPE_NOT_FOUND'
STATUS_UNKNOWN = 'ERROR_STATUS_UNKNOWN'
ERROR_UNKNOWN = 'ERROR_UNKNOWN'


class DispensersModel():
    """ Manage the dispensers.json data model from SCA Tork Easycube API
    """

    filename = os.path.join(
        AltF1BeHelpers.input_directory(
            [
                os.path.dirname(os.path.realpath(__file__)),
                'models',
                'sca-tork-easycube-api-model-dispensers'
            ]
        ), "dispensers.json"
    )

    def load(self, filename):
        """load a json file containing the data collected from SCA Tork Easycube /api/site/Dispensers

        """
        logger.info(f"load json: {filename}")
        self.filename = filename
        self.dispensers_json = ""
        with open(filename) as json_file:
            self.dispensers_json = json.load(json_file)

        return self.dispensers_json

    def __init__(self):
        self.load(self.filename)

    def find_by_type(self, type):
        """
            find a dispenser profile based on its type

            Return
            ------
            {'type': 'B1', 'type_name': 'Bin', 'category': 'Bin', 'prefix': 'B'}

        """
        for dispenser in self.dispensers_json['dispensers'][0]['types']:
            if type == dispenser['type']:
                return dispenser

    def get_action(self, type, status):
        """
            Find the next action to perform on a specific dispenser
logging.basicConfig(filename='example.log',level=logging.INFO)
            Return
            ------
            str : 'No re-fill needed'
        """
        try:
            next_action = self.dispensers_json['dispensers'][1]['actions'][0]['categories'][self.find_by_type(type)[
                'action']][status]
            return next_action
        except KeyError:
            logger.exception(f"{sys.exc_info()}")
            return STATUS_UNKNOWN
        except TypeError:
            logger.exception(f"{sys.exc_info()}")
            return DISPENSER_TYPE_NOT_FOUND
        except:
            logger.exception(f"{sys.exc_info()}")
            return ERROR_UNKNOWN


if __name__ == "__main__":

    dispenser_types = ['H2', 'S4', 'B1', 'T2']

    dispenserModel = DispensersModel()

    # dispensers_json = dispenserModel.load(filename)
    for dispenser_type in dispenser_types:
        dispenser = dispenserModel.find_by_type(dispenser_type)
        if dispenser is None:
            logger.info(f"{DISPENSER_TYPE_NOT_FOUND} : {dispenser_type}")
            logger.info(f"exit the program")
            sys.exit(f"Error : {DISPENSER_TYPE_NOT_FOUND} : {dispenser_type}")
        logger.info(f"dispenser: {dispenser}")
        action = dispenser['action']
        for status in ['Green', 'Yellow', 'Red']:
            logger.info(
                f"next_action for the {dispenser['type_name']}, {status}: {dispenserModel.get_action(type=dispenser_type, status=status)}"
            )
