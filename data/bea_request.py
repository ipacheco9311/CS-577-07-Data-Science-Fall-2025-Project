from dataclasses import dataclass

@dataclass
class BureauEconomicAnalysisRequest:
    """ Request payload for Bureau of Economics API """
    user_id: str
    dataset_name: str
    table_name: str
    geo_fips: str
    year: str
    line_code: str