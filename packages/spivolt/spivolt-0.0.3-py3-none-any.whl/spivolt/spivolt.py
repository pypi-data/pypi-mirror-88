import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional
from .parameters.dates import DateFilter
from .api.base import DefaultAPI, APIInterface


class GSN:
    """
    A wrapper for a given GSN API. Provides the point of contact for the user to get data.
    """
    def __init__(self, api: APIInterface):
        """
        :param api: The API to use when getting data
        :type api: APIInterface
        """
        self.api = api

    def get_sites(self) -> pd.DataFrame:
        """
        Get all the sites in the database.
        :return: A pandas DataFrame containing all the known sites
        :rtype: pandas.DataFrame
        """
        return pd.read_json(
            self.api.sites(),
            dtype={
                "id": np.uint,
                "name": str,
                "description": str,
                "location": str,
                "insar_available": np.bool,
                "owner": str,
                "num_sensors": np.uint
            }
        )

    def get_site(self, site_id: str) -> pd.DataFrame:
        """
        Get information about a specific site.
        :param site_id: The GSN ID of the site, usually the same as the job number
        :type site_id: str
        :return: A pandas DataFrame containing information about the specified site
        :rtype: pandas.DataFrame
        """
        return pd.read_json(
            self.api.sites(site_id),
            dtype={
                "id": np.uint,
                "name": str,
                "description": str,
                "location": str,
                "insar_available": np.bool,
                "owner": str,
                "num_sensors": np.uint
            }
        )

    def get_raw_sp_for_site(self,
                            site_id: str,
                            start: Optional[datetime] = None,
                            end: Optional[datetime] = None) -> pd.DataFrame:
        """
        Get unmodified SP data for a given site, optionally within a specific period of time.
        :param site_id: The GSN ID of the site, usually the same as the job number
        :type site_id: str
        :param start: An lower bound on the readings to return
        :type start: datetime
        :param end: An upper bound on the readings to return
        :type end: datetime
        :return: A pandas DataFrame containing SP data for the specified site
        :rtype: pandas.DataFrame
        """
        return pd.read_json(
            self.api.sp(site_id, DateFilter(start, end)),
            dtype={
                "pot_number": np.uint,
                "time": np.datetime64,
                "potential": np.single,
                "units": str,
                "pot_notes": Optional[str],
                "site_id": np.uint
            },
            convert_dates=["time", ]
        )


def connect_to_gsn(url: str, code: str, api=DefaultAPI) -> GSN:
    """
    Create a connection to the GSN API to use as the main access point for retrieving data.
    :param url: URL of the API
    :type url: str
    :param code: Access token for the API
    :type code: str
    :param api: The underlying wrapper the GSN object will use for connections
    :type api: Type(APIInterface)
    :return: An instantiated GSN object
    :rtype: GSN
    """
    return GSN(api(url, code))
