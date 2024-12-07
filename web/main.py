import httpx
import os
import pandas as pd
import streamlit as st
import plotly.express as px
import requests

from scipy.stats import ttest_ind, mannwhitneyu

from utils.graphs import *
from utils.api_requests import *

st.set_page_config(page_title="Covid-19 Data Analysis")

data = get_all_data("http://127.0.0.1:1234", "2010-01-01", "2025-01-01")
nans = get_nans_data("http://127.0.0.1:1234")
pies_data = get_pies_data("http://127.0.0.1:1234")

data.date = pd.to_datetime(data.date)
data[NUM_COLUMNS] = data[NUM_COLUMNS].apply(pd.to_numeric, axis=1)

deaths_by_years = data.groupby("year").deaths_by_cases.mean()
data_by_month = data.groupby("month")[NUM_COLUMNS].mean()
data_by_year = data.groupby("year")[NUM_COLUMNS].mean()
geo_data = data.loc[data.date.apply(lambda x: x.year == 2022 and x.month == 12 and x.day == 31)]

st.title('Covid-19 Data Analysis')
st.write('This is a simple dashboard to analyze Covid-19 data.')

st.dataframe(data)

st.text("The data on GDP (Gross Domestic Product) used in the analysis comes from two reliable sources:")

st.markdown(
    "1. The World Bank provides comprehensive GDP data through its official DataBank. The data series"
    " represents GDP in current US dollars for various countries and territories. "
    "This source is widely regarded for its accuracy and global coverage, ensuring high-quality and standardized data. "
    "The dataset can be accessed through [this link]"
    "(https://databank.worldbank.org/reports.aspx?source=2&series=NY.GDP.MKTP.CD&country)."
)

st.markdown(
    "2. Kaggle Dataset - GDP by Country 1999-2022. This dataset, available on Kaggle, contains historical GDP data for "
    "countries from 1999 to 2022. It aggregates GDP values from various official sources and presents them in a "
    "structured format suitable for analysis. This dataset is particularly useful for longitudinal studies and "
    "comparisons across multiple years. The dataset is accessible [here]"
    "(https://www.kaggle.com/datasets/alejopaullier/-gdp-by-country-1999-2022)."
)
st.text(
    "By combining these sources, the analysis benefits from both the reliability of the World Bank's official data "
    "and the extended historical perspective offered by Kaggle's dataset. "
    "This ensures robustness and comprehensiveness in the study of GDP-related trends."
)
st.dataframe(data.describe())

st.text(
    "The dataset includes 254,420 records spanning from January 5, 2020, to December 31, 2022. "
    "The average date is July 3, 2021, indicating an even distribution of data over time."
)
st.text(
    "The total number of cases (total_cases) ranges from 0 to 99,019,490, "
    "with an average of approximately 1,054,281. There is significant variability, "
    "as 50% of the records have fewer than 22,627 cases, and 75% have fewer than 297,111. "
    "New cases (new_cases) also show a wide range, from 0 to 40,475,480,"
    " with an average of 2,768. The high standard deviation indicates large "
    "fluctuations in the number of new cases."
)
st.text(
    "The total number of deaths (total_deaths) varies from 0 to 1,079,976, "
    "with an average of 15,525. Most records (50%) have fewer than 282 deaths,"
    " and 75% have fewer than 4,544, highlighting substantial differences. "
    "New deaths (new_deaths) peak at 28,982, with an average of 26.29, "
    "though many records report no new deaths."
)
st.text(
    "Metrics per million people (cases_per_million and deaths_per_million) "
    "reveal notable disparities between countries. Cases per million range from "
    "0 to 6,512.45, while deaths per million range from 0 to 674,434.94. "
    "These figures reflect the varying scale of the pandemic and differences "
    "in data reporting methods."
)
st.text(
    "Overall, the data shows considerable variation between countries in terms of "
    "cases and deaths, both in absolute numbers and per capita metrics. "
    "These differences are likely influenced by population size, testing availability, "
    "healthcare systems, and reporting practices. The temporal coverage of the dataset "
    "spans the entire pandemic, enabling detailed analysis of its progression over time."
)
st.plotly_chart(construct_nans_bar(nans))
st.text(
    "This bar chart represents the amount of missing data for each year from 2020 to 2024. The y-axis shows the "
    "number of missing values, while the x-axis lists the years."
)

st.text(
    "The chart indicates a relatively consistent level of missing "
    "data from 2020 to 2022, with a slight "
    "increase i202 However, in 2024, the number of missing values "
    "significantly decreases. This trend may reflect "
    "improvements in data collection and reporting over time or a "
    "decrease in available data as fewer cases or records are reported in recent years."
)

st.text(
    "The peak in missing data during 2023 could indicate disruptions in data processes or challenges in "
    "maintaining complete records. Overall, this visualization highlights the variations in data completeness "
    "across the observed period."
)
st.plotly_chart(construct_nans_pies(pies_data))
st.text(
    "This visualization consists of four pie charts, "
    "each representing the proportion of missing data for specific "
    "COVID-19 metrics (new_cases, new_deaths, total_cases, and total_deaths) "
    "for the years 2020, 2021, 2022, and 2023. The percentages on the charts indicate the "
    "share of missing data for each metric in the corresponding year."
)
st.text(
    "In 2020, the majority of missing data is associated with new_cases (66.7%), "
    "while the remainder comes from new_deaths (33.3%)."
    " The metrics total_cases and total_deaths show no missing data. "
    "In 2021, the missing data is evenly split between new_cases and new_deaths, "
    "each contributing 50%. In 2022 and 2023, the dominance of missing data in new_cases "
    "slightly decreases (60% and 58.8%, respectively), while the share of new_deaths "
    "increases (40% and 41.2%). The metrics total_cases and total_deaths remain fully "
    "complete throughout all years."
)
st.text(
    "These charts highlight that missing data is concentrated in the new_cases and "
    "new_deaths metrics, while data for total_cases and total_deaths was collected "
    "with greater completeness. Over time, there is a trend toward a more balanced "
    "distribution of missing data between new_cases and new_deaths, which may "
    "indicate gradual improvements in the data collection process."
)

st.plotly_chart(
    construct_geo(
        geo_data, locations="iso_code",
        hover_name="location",
        size="total_deaths",
        color="continent",
        projection="natural earth",
        title="Total Cases by Country on 31.12.2022 (max)"
    )
)
st.text(
    "This map shows the absolute total number of COVID-19 cases reported by each country. "
    "Larger circles represent countries with higher total case numbers. "
    "North America, South America, Europe, and parts of Asia have larger circles, "
    "indicating they reported more cases in total. "
    "Smaller circles in Africa and parts of Southeast Asia reflect fewer total cases."
)
st.plotly_chart(
    construct_geo(
        geo_data, locations="iso_code",
        hover_name="location",
        size="total_cases",
        color="continent",
        projection="natural earth",
        title="Total Deaths by Country on 31.12.2022 (max)"
    )
)
st.text(
    "This map displays the total number of cases adjusted for population "
    "(cases per million people). Countries in Europe and parts of South "
    "America have larger circles, suggesting high case rates relative to "
    "their population. Smaller circles in Africa and Asia highlight lower "
    "per capita infection rates, which could reflect fewer cases or lower "
    "testing and reporting rates."
)
st.plotly_chart(
    construct_geo(
        geo_data, locations="iso_code",
        hover_name="location",
        size="total_deaths_per_million",
        color="continent",
        projection="natural earth",
        title="Total Deaths by Country on 31.12.2022 per million (max)"
    )
)
st.text(
    "This visualization focuses on the countries with the highest reported total cases. "
    "Regions such as North America and Europe have the most prominent circles, "
    "indicating their leading position in absolute case counts globally. "
    "The emphasis is on identifying areas with the most severe outbreaks."
)
st.plotly_chart(
    construct_geo(
        geo_data, locations="iso_code",
        hover_name="location",
        size="total_cases_per_million",
        color="continent",
        projection="natural earth",
        title="Total Cases by Country on 31.12.2022 per million (max)"
    )
)
st.text(
    "Similar to the second map, this one emphasizes the maximum case rates per million people. "
    "It highlights how some smaller countries or regions with high case density stand out,"
    " especially in Europe and South America, where the relative impact of the pandemic was "
    "more significant on a per capita basis."
)
st.plotly_chart(
    px.pie(
        data,
        names="continent",
        title="Distribution of Covid Data by Continents"
    )
)
st.plotly_chart(
    px.bar(
        deaths_by_years,
        x=deaths_by_years.index.astype(str),
        y=deaths_by_years.values,
        title="Mean Deaths by Cases by Year"
    )
)
st.text(
    "This bar chart illustrates the mean ratio of deaths to cases (deaths_by_cases) "
    "by year, providing insight into the lethality of COVID-19 in different periods."
)
st.text(
    "In 2020, the mean deaths by cases ratio is significantly higher compared to "
    "subsequent years, indicating that the virus had a much greater impact in "
    "terms of mortality relative to reported cases during the early stages of the pandemic. "
    "This may be attributed to limited medical knowledge, inadequate treatments, "
    "and strained healthcare systems at the onset of the pandemic."
)
st.text(
    "In 2021 and 2022, the mean deaths by cases ratio drops substantially. "
    "This decline suggests improved pandemic management, including the widespread "
    "rollout of vaccines, advancements in treatment methods, and potentially better "
    "testing and reporting of cases. The consistency between 2021 and 2022 highlights "
    "that these improvements were sustained over time."
)
st.text(
    "Overall, the chart shows a dramatic reduction in the lethality of COVID-19 after 2020, "
    "reflecting global efforts to mitigate the virus's impact on mortality."
)
st.plotly_chart(
    construct_all_data_hists(data_by_month)
)
st.text(
    "This chart displays the average values of four COVID-19 metrics "
    "(total_cases, new_cases, total_deaths, and new_deaths) "
    "by month over a three-year period. Each graph represents the "
    "average monthly trend for one of these metrics throughout the year."
)
st.text(
    "The total_cases graph shows a steady increase in cases month by month. "
    "This reflects the cumulative nature of total cases over time, averaged "
    "across the three years. The upward trend continues towards the end of the year."
)
st.text(
    "In the new_cases graph, sharp peaks are observed at the beginning of the year, "
    "followed by a decline and stabilization in the middle months. "
    "Towards the end of the year, there is another significant rise in new cases, "
    "which may indicate seasonal spikes in the spread of the infection."
)
st.text(
    "The total_deaths graph follows a similar pattern, with a consistent increase "
    "in the average number of deaths across months. "
    "This trend reflects the cumulative nature of this metric as well."
)
st.text(
    "The new_deaths graph shows fluctuations, with noticeable peaks at the "
    "beginning and end of the year. This indicates that certain periods "
    "(possibly seasonal waves) significantly influence mortality. "
    "The average values remain relatively stable during the middle months."
)
st.text(
    "Overall, these graphs illustrate how the pandemic unfolded over the course "
    "of a year on average across three years. Cumulative metrics like total "
    "cases and deaths consistently rise, while new cases and deaths exhibit"
    " more pronounced peaks during specific times of the year."
)
st.plotly_chart(
    construct_all_data_hists(data_by_year)
)
st.text(
    "This chart shows four bar graphs representing COVID-19 metrics: "
    "total cases, new cases, total deaths, "
    "and new deaths from 2020 to 2022. Total cases and total deaths "
    "steadily increased over the years, reflecting the cumulative nature of the pandemic. "
    "New cases rose sharply in 2022, reaching their highest level, showing the continued "
    "spread of the virus."
)
st.text(
    "New deaths peaked in 2021 but decreased in 2022. "
    "This decline likely reflects the positive impact of vaccination "
    "efforts, which were completed by 2022. "
    "Overall, the chart highlights the pandemic's growth while suggesting progress "
    "in controlling its deadliest effects by 2022."
)

st.plotly_chart(
    corr(data)
)
st.text(
    "The variable gdp shows a moderate positive correlation with total_deaths and total_cases. "
    "This indicates that countries with higher GDP tend to report higher absolute numbers of "
    "deaths and cases, which may be attributed to better reporting systems and broader testing "
    "capacity in wealthier nations."
)
st.text(
    "When normalized by population (total_deaths_per_million and total_cases_per_million), the correlation with "
    "gdp becomes weaker. This suggests that GDP has a less direct relationship with per capita metrics, potentially "
    "reflecting the impact of advanced healthcare systems and effective public health measures in reducing mortality "
    "and case rates in high-GDP countries."
)
st.title("GDP Analysis (Hypothesis Testing)")
st.text(
    "The COVID-19 mortality rate per million people depends on a country's GDP level. "
    "Countries with higher GDP levels are likely to have lower mortality rates per million "
    "people due to better access to healthcare services and more effective pandemic control "
    "measures."
)
data_test = data.loc[(data.new_deaths != 0) & (data.total_deaths_per_million != 0)]
data_test = data_test.dropna(subset=['total_deaths_per_million', 'gdp']).copy()
data_test = data_test.drop_duplicates(subset=['iso_code', 'date']).copy()
data_test = data_test.sort_values(by=['iso_code', 'date']).copy()

data_test['gdp_group'] = pd.qcut(data_test['gdp'], q=3, labels=['Low', 'Medium', 'High'])

data_test['spread_rate_per_million'] = data_test.groupby('iso_code')['total_deaths_per_million'].diff()
data_test = data_test[data_test['spread_rate_per_million'] > 0].copy()

spread_rates = data_test.groupby('gdp_group')['spread_rate_per_million'].mean()
st.text("Average spread rate per million for GDP groups:")

st.dataframe(spread_rates.reset_index())

low = data_test[data_test['gdp_group'] == 'Low']['spread_rate_per_million'].dropna()
medium = data_test[data_test['gdp_group'] == 'Medium']['spread_rate_per_million'].dropna()
high = data_test[data_test['gdp_group'] == 'High']['spread_rate_per_million'].dropna()

st.text("Pairwise T-tests:")
t_stat_low_medium, p_value_low_medium = ttest_ind(low, medium, equal_var=False)
st.text(f"Low vs. Medium: t_stat = {t_stat_low_medium}, p_value = {p_value_low_medium}")

t_stat_medium_high, p_value_medium_high = ttest_ind(medium, high, equal_var=False)
st.text(f"Medium vs. High: t_stat = {t_stat_medium_high}, p_value = {p_value_medium_high}")

t_stat_low_high, p_value_low_high = ttest_ind(low, high, equal_var=False)
st.text(f"Low vs. High: t_stat = {t_stat_low_high}, p_value = {p_value_low_high}")

st.text("Pairwise Mann-Whitney U-tests:")
u_stat_low_medium, p_value_u_low_medium = mannwhitneyu(low, medium, alternative='two-sided')
st.text(f"Low vs. Medium: u_stat = {u_stat_low_medium}, p_value = {p_value_u_low_medium}")

u_stat_medium_high, p_value_u_medium_high = mannwhitneyu(medium, high, alternative='two-sided')
st.text(f"Medium vs. High: u_stat = {u_stat_medium_high}, p_value = {p_value_u_medium_high}")

u_stat_low_high, p_value_u_low_high = mannwhitneyu(low, high, alternative='two-sided')
st.text(f"Low vs. High: u_stat = {u_stat_low_high}, p_value = {p_value_u_low_high}")

st.text(
    "The hypothesis that the COVID-19 mortality rate per million people depends on a "
    "country's GDP level is partially confirmed. Pairwise T-tests show significant "
    "differences in mean mortality rates across all three GDP groups, with very low "
    "p-values for all comparisons. However, the Mann-Whitney U-tests reveal no "
    "significant difference in the distributions of mortality rates between Low "
    "and Medium GDP groups, despite the difference in their means. This suggests "
    "that while GDP level influences mortality rates, additional factors may play "
    "a role, requiring further investigation."
)

st.title("New Data Submission")

with st.form("api_form"):
    iso_code = st.text_input("ISO Code")
    continent = st.selectbox("Continent", ["Asia", "Europe", "Africa", "Oceania", "North America", "South America"])
    location = st.text_input("Location")
    date = st.date_input("Date")
    population = st.number_input("Population", min_value=0, step=1)
    total_cases = st.number_input("Total Cases", min_value=0, step=1)
    new_cases = st.number_input("New Cases", min_value=0, step=1)
    total_deaths = st.number_input("Total Deaths", min_value=0, step=1)
    new_deaths = st.number_input("New Deaths", min_value=0, step=1)
    total_deaths_per_million = st.number_input("Total Deaths per Million", min_value=0.0, step=0.1)
    total_cases_per_million = st.number_input("Total Cases per Million", min_value=0.0, step=0.1)

    submitted = st.form_submit_button("Submit")

if submitted:
    payload = {
        "iso_code": iso_code,
        "continent": continent,
        "location": location,
        "date": str(date),
        "day": date.day,
        "month": date.month,
        "year": date.year,
        "deaths_by_cases": total_deaths / total_cases if total_cases != 0 else 0,
        "population": population,
        "total_cases": total_cases,
        "new_cases": new_cases,
        "total_deaths": total_deaths,
        "new_deaths": new_deaths,
        "total_deaths_per_million": total_deaths_per_million,
        "total_cases_per_million": total_cases_per_million,
    }

    try:
        response = requests.post("http://127.0.0.1:8000/api/v1/data", json=payload)

        if response.status_code == 200:
            st.success("Data successfully submitted!")
        else:
            st.error(f"Error: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
