import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.subplots as sp

from sklearn.preprocessing import LabelEncoder

__all__ = (
    "construct_nans_bar",
    "construct_nans_pies",
    "construct_geo",
    "construct_all_data_hists",
    "NUM_COLUMNS",
    "USEFUL_COLUMNS",
    "corr"
)

_PIE_COLUMNS = ["date", "total_cases", "new_cases", "total_deaths", "new_deaths"]
_NUM_COLUMNS = ["total_cases", "new_cases", "total_deaths", "new_deaths"]

NUM_COLUMNS = _NUM_COLUMNS.copy()
USEFUL_COLUMNS = [
    "iso_code",
    "continent",
    "location",
    "date",
    "total_cases",
    "new_cases",
    "total_deaths",
    "new_deaths",
    "total_deaths_per_million",
    "total_cases_per_million",
]


def construct_nans_bar(data: dict) -> go.Figure:
    return px.bar(
        x=data.keys(), y=data.values(), title="Missing Data by Years"
    )


def construct_nans_pies(data: dict) -> go.Figure:
    subplot = sp.make_subplots(
        rows=2, cols=2, specs=[
            [{"type": "domain"}, {"type": "domain"}],
            [{"type": "domain"}, {"type": "domain"}],
        ],
        subplot_titles=["2020", "2021", "2022"]
    )
    for year, values in data.items():
        subplot.add_trace(
            go.Pie(
                labels=data[year]["labels"],
                values=data[year]["values"],
                name=data[year]["name"]
            ),
            row=data[year]["row"],
            col=data[year]["col"]
        )

    subplot.update_layout(title_text="Missing Data by Years (without all nans)")
    return subplot


def construct_geo(
    data,
    *,
    locations: str,
    hover_name: str,
    size: str,
    color: str,
    projection: str,
    title: str
) -> go.Figure:
    return px.scatter_geo(
        data,
        locations=locations,
        hover_name=hover_name,
        size=size,
        color=color,
        projection=projection,
        title=title,
        template="plotly_dark"
    )


def construct_all_data_hists(data: pd.DataFrame) -> go.Figure:
    subplot = sp.make_subplots(
        rows=2, cols=2, subplot_titles=_NUM_COLUMNS
    )
    for i in range(len(_NUM_COLUMNS)):
        subplot.add_trace(
            go.Bar(
                x=data.index,
                y=data[_NUM_COLUMNS[i]],
                name=_NUM_COLUMNS[i]
            ),
            row=(i // 2) + 1, col=(i % 2) + 1
        )

    return subplot

def corr(data: pd.DataFrame):
    le_location = LabelEncoder()
    le_continent = LabelEncoder()
    corr_data = data.copy()
    corr_data["location"] = le_location.fit_transform(corr_data.location)
    corr_data["continent"] = le_continent.fit_transform(corr_data.continent)
    fig = px.imshow(corr_data.drop("iso_code", axis=1).corr())
    return fig