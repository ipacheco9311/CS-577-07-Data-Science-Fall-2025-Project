from __future__ import annotations
from dotenv import dotenv_values
from ucimlrepo import fetch_ucirepo
import beaapi

class UcIrvineAPI:

    def __init__(self):
        pass

    @staticmethod
    def fetch_dataset(repo_id: int | None = None):
        """
        Loads a dataset from the UCI ML Repository, including the dataframes and metadata information
        :param repo_id: Dataset ID for UCI ML Repository
        :return: object containing dataset metadata, dataframes, and variable info in its properties
        """
        return fetch_ucirepo(id=repo_id)

class BureauEconomicAnalysisAPI:

    def __init__(self):
        pass

    @staticmethod
    def fetch_dataset():
        """
            Loads a dataset from the Bureau of Economic Analysis API, including the dataframes and metadata information
            :return: a dataframe containing real personal income of all U.S. states in 2019
         """
        user_id = dotenv_values()["beakey"]
        dataset_name = 'Regional'
        kwargs = {
            'GeoFips': 'STATE',
            'LineCode': '1',
            'TableName': 'SARPP',
            'Year': '2019'
        }
        return beaapi.get_data(user_id, dataset_name, **kwargs)
