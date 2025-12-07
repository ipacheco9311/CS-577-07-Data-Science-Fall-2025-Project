from __future__ import annotations
from ucimlrepo import dotdict
from ucimlrepo import fetch_ucirepo
from enum import IntEnum


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
