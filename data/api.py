from __future__ import annotations
from ucimlrepo import fetch_ucirepo
import beaapi
from data.bea_request import BureauEconomicAnalysisRequest as BEARequest
import pandas as pd

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
    def fetch_dataset(request: BEARequest) -> pd.DataFrame:
        """Fetch BEA data and return it as a pandas DataFrame."""
        if not request.user_id:
            raise ValueError("BEA API key is required.")

        params = {
            "TableName": request.table_name,
            "GeoFips": request.geo_fips,
            "Year": request.year,
            "LineCode": request.line_code
        }

        return beaapi.get_data(
            userid=request.user_id,
            datasetname=request.dataset_name,
            **params
        )