import os
import fastapi
import pandas as pd

from datetime import datetime
from pydantic import BaseModel

from utils.data import *

app = fastapi.FastAPI()

if not os.path.exists(os.environ.get("deaths_filename", "")):
    raise Exception("Deaths file not found")
if not os.path.exists(os.environ.get("gdp_filename", "")):
    raise Exception("GDP file not found")
if not os.path.exists(os.environ.get("gdp2_filename", "")):
    raise Exception("GDP2 file not found")

gdp = load_gdp(os.environ["gdp_filename"])
gdp2 = pd.read_csv(os.environ["gdp2_filename"])
deaths = load_deaths(
    os.environ["deaths_filename"],
    gdp=gdp,
    gdp2=gdp2,
    years=[
        "2020",
        "2021",
        "2022",
    ]
)


class Item(BaseModel):
    iso_code: str
    continent: str
    location: str
    date: datetime
    day: int
    month: int
    year: int
    deaths_by_cases: float
    population: int
    total_cases: int
    new_cases: int
    total_deaths: int
    new_deaths: int
    total_deaths_per_million: float
    total_cases_per_million: float


@app.get("/api/v1/data")
def read_data(
    start_datetime: datetime,
    end_datetime: datetime,
):
    data = deaths.loc[
        (deaths.date >= start_datetime) & (deaths.date <= end_datetime)
        ]
    return data.fillna('').to_dict()


@app.get("/api/v1/nans-counts")
def get_nans_value_counts():
    return get_bar_data(os.environ["deaths_filename"])


@app.get("/api/v1/get-pies-data")
def get_nans_value_counts():
    return get_pies_data(os.environ["deaths_filename"])


@app.post("/api/v1/data")
def create_data(item: Item):
    global deaths

    new_data = pd.DataFrame([item.model_dump()])
    deaths = pd.concat([deaths, new_data], ignore_index=True)

    return {"message": "Data created successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
