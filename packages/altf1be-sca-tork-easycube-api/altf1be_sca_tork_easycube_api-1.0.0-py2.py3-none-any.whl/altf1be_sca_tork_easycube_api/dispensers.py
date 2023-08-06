# *-* coding:utf-8 *-*

from .sca_tork_easycube_api import SCATorkEasyCubeAPI
import logging
import time
import pandas as pd
from .dispensers_model import DispensersModel
from datetime import datetime
from altf1be_helpers import AltF1BeHelpers
from .sca_tork_easycube_api_helpers import SCATorkEasyCubeAPIHelpers
from pytz import timezone
import glob
import json
import numpy as np
import os

import sys
sys.path.append(os.path.join(os.getcwd()))


log_filename = AltF1BeHelpers.create_append_log_file(
    f"{os.path.basename(__file__)}.log"
)

logger = AltF1BeHelpers.get_logger(
    log_level=logging.INFO,
    # log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_filename=log_filename
)


class Dispensers(SCATorkEasyCubeAPI, SCATorkEasyCubeAPIHelpers):
    """create the df containing the dispensers"""

    dispensers_model_path = os.path.join(
        AltF1BeHelpers.input_directory(
            ["models", "sca-tork-easycube-api-model-dispensers"]
        ),
        "dispensers.json",
    )

    def get_dispenser_model(self, dispenserType="B1"):
        # keep: load the business rules of the dispenser of SCA Tork Easycube API

        self.dispenserModel = DispensersModel()
        # dispenser_json = self.dispenserModel.load(self.dispensers_model_path)
        # dispenser = dispenserModel.find_by_type(dispenserType)

    def get_actions(self, dispenserType="B1"):

        # keep: load the business rules of the dispenser of SCA Tork Easycube API

        # dispenser = dispenserModel.find_by_type(dispenserType)
        data_str = self.get_api_data("/api/site/Dispensers")
        dispensers_json = json.loads(data_str)

        df = self.create_df_from_json(dispensers_json)

        return df

    def create_df(self, filename_full_path):
        # filename_full_path = r'/kaggle/input/2020-06-11_13-45-04-sca-tork-easycube-dispensers.json'
        filename = os.path.basename(filename_full_path)
        # logger.info(f'valid_date(): {valid_date(filename)}, valid_time(): {valid_time(filename)}')
        data = json.load(
            open(
                filename_full_path
            ),
            parse_int=False
        )
        df = pd.DataFrame(data["result"]["dispensers"])

        df["date"] = AltF1BeHelpers.valid_date(filename)
        df["time"] = AltF1BeHelpers.valid_time(filename)
        df[
            "datetime_str"
        ] = f'{AltF1BeHelpers.valid_date(filename)} {AltF1BeHelpers.valid_time(filename).replace("-",":")}'
        df["epoch"] = df["datetime_str"].apply(
            lambda x: int(time.mktime(time.strptime(x, "%Y-%m-%d %H:%M:%S")))
        )
        df["datetime"] = df["epoch"].apply(
            lambda epoch: datetime.fromtimestamp(epoch))
        df["datetime15"] = df["datetime"].apply(
            lambda dt: datetime(
                dt.year, dt.month, dt.day, dt.hour, 15 * (dt.minute // 15)
            )
        )
        # df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        return df

    def create_df_from_json(self, data):
        """Create df based on a json string"""
        now = datetime.now()  # .replace(tzinfo=timezone('Europe/Brussels'))
        if len(data) == 0:
            column_names = [
                "status",
                "date",
                "time",
                "datetime_str",
                "epoch",
                "datetime",
                "datetime15",
            ]
            df = pd.DataFrame(columns=column_names)
        else:
            df = pd.DataFrame(data["result"]["dispensers"])

            df["date"] = now.strftime("%Y-%m-%d")
            df["time"] = now.strftime("%Hh%M")
            df["datetime_str"] = now.strftime("%Y-%m-%d %Hh%M")
            df["epoch"] = now.timestamp()
            df["datetime"] = df["epoch"].apply(
                lambda epoch: datetime.fromtimestamp(epoch)
            )
            df["datetime15"] = df["datetime"].apply(
                lambda dt: datetime(
                    dt.year, dt.month, dt.day, dt.hour, 15 * (dt.minute // 15)
                )
            )
            # df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        return df

    def __init__(self):
        super().__init__()
        self.get_dispenser_model()

    def build_df(self):
        # keep
        # build df for dispensers
        data_directory = ""
        filenames_pattern = "*-sca-tork-easycube-dispensers.json"
        if AltF1BeHelpers.is_interactive():
            input_directory = "/kaggle/input"
            sca_tork_directory = "sca-tork-easycube-api"
            sca_tork_directory_version = "2020-06-12-10h03"
            data_directory = os.path.join(
                input_directory,
                sca_tork_directory,
                sca_tork_directory_version,
                "**",
                filenames_pattern,
            )
        else:
            data_directory = os.path.join(
                AltF1BeHelpers.input_directory([]), "**", filenames_pattern
            )
        # count_files_in_dir(data_directory)

        # keep build df for dispensers
        dispensers_filenames = glob.glob(data_directory, recursive=True)
        if len(dispensers_filenames) == 0:
            logger.info(
                f"There are 0 dispensers data available in {data_directory}")
            exit()
        logger.info(
            f"length of dispensers_filenames # : {len(dispensers_filenames)}")
        df = pd.DataFrame()
        for filename in dispensers_filenames:
            # logger.info(f'filename: {filename}')
            df = pd.concat([df, self.create_df(filename)])
        df = df.sort_values("epoch")
        logger.info(f"df is sorted and created")

        # create range every 15 minutes from Min time in df to Max time
        date_rng = pd.date_range(
            start=df["datetime15"].min(), end=df["datetime15"].max(), freq="15min"
        )

        # keep
        # we keep the first dataset closest to the 15 minutes range

        df_fifteen = pd.DataFrame()
        for current_date in date_rng:
            df_fifteen = df[df["datetime15"] == current_date]
            # remove the rows including the epoch (min) we want to keep
            unique_epochs = df_fifteen["epoch"].unique()
            if len(unique_epochs) > 0:
                epochs_to_remove = np.delete(unique_epochs, [0])
            # logger.info(epochs_to_remove)
            # keep the first set of data stored during the same range (remove rows stored from 12:00 to 12:15)
            df = df.loc[~df["epoch"].isin(epochs_to_remove)]
        return df

    def print_actions(self, df):
        """print Green, Yellow and Red actions as tables"""

        # keep latest information
        df = df.loc[df["epoch"] == df["epoch"].max()]

        self.df_green = df[df["status"] == "Green"]
        self.df_yellow = df[df["status"] == "Yellow"]
        self.df_red = df[df["status"] == "Red"]

        # keep : list the actions per item

        logger.info(f"{self.df_red.shape[0]} immediate action(s) : Red")
        for index, row in self.df_red.iterrows():
            logger.info(
                f"{row['dispenserType']}, {row['dispenserName']}, {row['status']}, {self.dispenserModel.get_action(type=row['dispenserType'], status=row['status'])}"
            )

        if self.df_yellow.size > 0:
            logger.info(f"{self.df_yellow.iloc[0]['datetime15']}")
        logger.info(f"{self.df_yellow.shape[0]} urgent action(s) : Yellow")
        for index, row in self.df_yellow.iterrows():
            logger.info(
                f"{row['dispenserType']}, {row['dispenserName']}, {row['status']}, {self.dispenserModel.get_action(type=row['dispenserType'], status=row['status'])}"
            )

    def get_dashboard_json(self, df):
        """
        generate a json containing the data displayed on the dashboard
        """

        data_json = [
            {
                "id": 1,
                "color": "red",
                "count": len(df[df["status"] == "Red"]),
                "msg": "Immediate action(s)",
                "url": "sca_tork_easycube_api.actions",
                "is_empty": df[df["status"] == "Red"].empty,
            },
            {
                "id": 2,
                "color": "yellow",
                "count": len(df[df["status"] == "Yellow"]),
                "msg": "Requires attention",
                "url": "sca_tork_easycube_api.actions",
                "is_empty": df[df["status"] == "Yellow"].empty,
            },
            {
                "id": 3,
                "color": "navy",
                "count": len(df[df["status"] == "Green"]),
                "msg": "Doing fine",
                "url": "sca_tork_easycube_api.actions",
                "is_empty": df[df["status"] == "Green"].empty,
            },
        ]
        dispensers_count_not_empty = (
            (1 if df[df["status"] == "Red"].empty is False else 0)
            + (1 if df[df["status"] == "Yellow"].empty is False else 0)
            + (1 if df[df["status"] == "Green"].empty is False else 0)
        )

        return data_json, dispensers_count_not_empty


if __name__ == "__main__":
    dispensers = Dispensers()

    df_actions = dispensers.get_actions()
    dispensers.print_actions(df_actions)

    df = dispensers.build_df()
    logger.info(f"dispensers.df: {df}")
