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
        :param repo_id: Dataset ID for UCI ML Repositor
        :return: object containing dataset metadata, dataframes, and variable info in its properties
        """
        return fetch_ucirepo(id=repo_id)

class BureauEconomicAnalysisAPI:

    def __init__(self):
        pass

    @staticmethod
    def get_data_set_list():
        beakey = dotenv_values()["beakey"]
        return beaapi.get_data_set_list(beakey)

    @staticmethod
    def get_parameter_list(dataset_name):
        beakey = dotenv_values()["beakey"]
        return beaapi.get_parameter_list(beakey, dataset_name)

    @staticmethod
    def get_parameter_values(dataset_name, parameter_name):
        beakey = dotenv_values()["beakey"]
        return beaapi.get_parameter_values(beakey, dataset_name, parameter_name)

    @staticmethod
    def get_parameter_metadata(dataset_name, target_parameter, **kwargs):
        beakey = dotenv_values()["beakey"]
        return beaapi.get_parameter_values_filtered(beakey, dataset_name, target_parameter, **kwargs)

    @staticmethod
    def fetch_data(dataset_name, **kwargs):
        beakey = dotenv_values()["beakey"]
        return beaapi.get_data(beakey, dataset_name, **kwargs)
