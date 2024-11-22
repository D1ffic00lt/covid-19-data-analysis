import numpy as np
import pandas as pd

__all__ = ("load_deaths", "load_gdp")
_NUMERIC_COLUMNS = [
    "total_cases", "new_cases",
    "total_deaths", "new_deaths",
    "total_cases_per_million",
    "new_cases_per_million",
    "total_deaths_per_million"
]
_GDP_COLUMNS = {
    "1990 [YR1990]": "1990",
    "2000 [YR2000]": "2000",
    "2014 [YR2010]": "2010",
    "2015 [YR2015]": "2015",
    "2016 [YR2016]": "2016",
    "2017 [YR2017]": "2017",
    "2018 [YR2018]": "2018",
    "2019 [YR2019]": "2019",
    "2020 [YR2020]": "2020",
    "2021 [YR2021]": "2021",
    "2022 [YR2022]": "2022",
    "2023 [YR2023]": "2023",
}


def _get_deaths_by_cases(data_columns):
    result = np.zeros(data_columns.shape[0])

    row_deaths = data_columns.total_deaths
    row_cases = data_columns.total_cases

    zeros_indexes = (row_cases == 0)
    result[zeros_indexes] = 0
    result[~zeros_indexes] = row_deaths[~zeros_indexes] / row_cases[~zeros_indexes]
    return result


def _get_gdp(row: pd.Series):
    return row[str(row.date.year)]


def load_deaths(
    path: str,
    *,
    gdp: pd.DataFrame,
    gdp2: pd.DataFrame,
    years: list = None
) -> pd.DataFrame:
    if years is None:
        years = ["2020", "2021", "2022"]
    max_year = max(map(int, years))
    deaths = pd.read_csv(path)
    deaths[_NUMERIC_COLUMNS] = deaths[_NUMERIC_COLUMNS].apply(pd.to_numeric, errors="coerce")
    deaths.date = pd.to_datetime(deaths.date)
    deaths = deaths.loc[deaths.iso_code.apply(lambda x: "OWID" not in x)]
    deaths = deaths.loc[deaths.date.apply(lambda x: x.year < (max_year + 1))]
    deaths["year"] = deaths.date.apply(lambda x: x.year)
    deaths["month"] = deaths.date.apply(lambda x: x.month)
    deaths["day"] = deaths.date.apply(lambda x: x.day)

    deaths["deaths_by_cases"] = _get_deaths_by_cases(deaths[["total_deaths", "total_cases"]])

    locations = {}
    unique_names = gdp2.Country.unique()
    unused_locations = []

    for location in deaths.iso_code.unique():
        if location in gdp["Country Code"].unique():
            locations[location] = gdp.loc[gdp["Country Code"] == location, years].to_dict()
        else:
            name = deaths.loc[deaths.iso_code == location].location.values[0]

            for country in unique_names:
                if isinstance(country, float):
                    continue
                if name in country:
                    locations[name] = gdp2.loc[gdp2.Country == country, years].to_dict()
                    break
            else:
                unused_locations.append(location)
    for location in locations.keys():
        locations[location] = {k: list(v.values())[0] for k, v in locations[location].items()}

    gpd_dataframe = pd.DataFrame(locations).T.reset_index()
    deaths = deaths.merge(gpd_dataframe, left_on="iso_code", right_on="index")
    deaths = deaths.drop("index", axis=1)
    deaths["gdp"] = deaths.apply(_get_gdp, axis=1)
    deaths = deaths.drop(years, axis=1)
    deaths = deaths.loc[deaths.gdp != ".."]
    deaths["gdp"] = pd.to_numeric(deaths['gdp'], errors='coerce')

    return deaths


def load_gdp(path: str) -> pd.DataFrame:
    gdp = pd.read_csv(path)
    gdp = gdp.rename(_GDP_COLUMNS, axis=1)
    return gdp
