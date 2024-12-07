import httpx
import pandas as pd

__all__ = ("get_all_data", "get_nans_data", "get_pies_data")


def get_all_data(address: str, start_date: str, end_date: str):
    return pd.DataFrame.from_dict(
        httpx.get(
            address + "/api/v1/data", params={
                "start_datetime": start_date,
                "end_datetime": end_date
            }, timeout=30
        ).json()
    )


def get_nans_data(address: str):
    return httpx.get(address + "/api/v1/nans-counts", timeout=30).json()

def get_pies_data(address: str):
    return httpx.get(address + "/api/v1/get-pies-data", timeout=30).json()
