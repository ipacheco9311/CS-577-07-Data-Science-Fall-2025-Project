from __future__ import annotations
from ucimlrepo import fetch_ucirepo

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