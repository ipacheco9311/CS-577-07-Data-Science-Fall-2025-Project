from __future__ import annotations
from dotenv import dotenv_values
from ucimlrepo import dotdict
from ucimlrepo import fetch_ucirepo
from enum import IntEnum
import beaapi
from pandas import DataFrame


class UcIrvineAPI:
    @staticmethod
    def fetch_dataset(repo_id: int | None = None) -> dotdict:
        """
        Loads a dataset from the UCI ML Repository, including the dataframes and metadata information
        :param repo_id: Dataset ID for UCI ML Repository
        :return: object containing dataset metadata, dataframes, and variable info in its properties
        """
        return fetch_ucirepo(id=repo_id)


class UcIrvineDatasetIDs(IntEnum):
    """
    Enum for Dataset IDs in UCI's ML Repository .
    """
    Apartment_For_Rent_Classified = 555


class BureauEconomicAnalysisAPI:
    @staticmethod
    def fetch_dataset(dataset_name, **kwargs) -> DataFrame:
        """
            Loads a dataset from the Bureau of Economic Analysis API, including the dataframes and metadata information
            :param dataset_name – Name of BEA dataset
            :param kwargs – Other named parameters as key-value pairs
            :return:
            A table with data. The 'DataValue' col will try to be converted to a numeric using pd.to_numeric().
            '', '(NA)', and '(NM)'/'(D)' (when accompanied by the same in the NoteRef col) will be converted to np.nan.
         """
        user_id = dotenv_values()['BEA_KEY']
        return beaapi.get_data(user_id, dataset_name, **kwargs)
