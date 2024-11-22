import os
import fastapi
import pandas as pd

from datetime import datetime
from typing import Annotated

from utils.data import load_deaths, load_gdp
os.environ["deaths_filename"] = "./data/CovidDeaths.csv"
os.environ["gdp_filename"] = "./data/a4275215-339d-415e-a792-70f1f7215a5c_Data.csv"
os.environ["dpg2_filename"] = "./data/GDP by Country 1999-2022.csv"

app = fastapi.FastAPI()

if not os.path.exists(os.environ.get("deaths_filename", None)):
    raise Exception("Deaths file not found")
if not os.path.exists(os.environ.get("gdp_filename", None)):
    raise Exception("GDP file not found")
if not os.path.exists(os.environ.get("dpg2_filename", None)):
    raise Exception("GDP2 file not found")


gdp = load_gdp(os.environ["gdp_filename"])
gdp2 = pd.read_csv(os.environ["dpg2_filename"])
deaths = load_deaths(os.environ["deaths_filename"], gdp=gdp, gdp2=gdp2)


@app.get("/api/v1/data")
def read_data(
    start_datetime: datetime,
    end_datetime: datetime,
):
    data = deaths.loc[
        (deaths.date >= start_datetime) & (deaths.date <= end_datetime)
    ]
    return data.dropna().to_dict(orient="records")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
