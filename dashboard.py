#load necessary libraries
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
import re

#preprocessing

df = pd.read_csv("ds_jobs.csv")
#standardizing job titles
df["title"] = df["title"].str.lower()
df["title"] = df["title"].str.replace("sr.", "senior")
df["title"] = df["title"].str.replace(r"\b(i|ii|iii)\b", "", regex=True)
#grouping by job type
def job_type(title):
    title = str(title).lower()
    if "data scientist" in title or "data science" in title:
        return "Data Scientist"
    elif "data engineer" in title or "data engineering" in title:
        return "Data Engineer"
    elif "data analyst" in title or "data analysis" in title or "analyst" in title:
        return "Data Analyst"
    elif "machine learning scientist" in title or "machine learning science" in title:
        return "ML Scientist"
    elif "machine learning engineer" in title or "ml engineer" in title or "ml engineering" in title or "machine learning engineering" in title:
        return "ML Engineer"
    elif "ai engineer" in title or "ai engineering" in title:
        return "AI Engineer"
    elif "ai/ml engineer" in title or "ai/ml engineering" in title:
        return "AI/ML Engineer"
    elif "deep learning" in title:
        return "Deep Learning Engineer"
    elif "big data engineer" in title or "big data engineering" in title:
        return "Big Data Engineer"
    elif "analytics engineer" in title or "analytics engineering" in title:
        return "Analytics Engineer"
    elif "business analyst" in title or "business analysis" in title:
        return "Business Analyst"
    elif "bi analyst" in title or "business intelligence" in title or "bi analysis" in title or "business intelligence analysis" in title:
        return "Business Intelligence Analyst"
    elif "software engineer" in title or "software engineering" in title:
        return "Software Engineer"
    elif "data manager" in title or "manager" in title or "data management" in title or "management" in title:
        return "Data Manager"
    elif "cloud" in title:
        return "Cloud Engineer"
    elif "database" in title or "db" in title:
        return "Database Engineer"
    else:
        return "Other"
df["job_type"] = df["title"].apply(job_type)
#extract years of experience from description
df["description"] = df["description"].str.lower()
def extract_experience(description, title = ""):
    if pd.isna(description):
        return None
    description = description.lower()
    title = str(title).lower()
    #handle a range like 5-7 years
    range_match = re.search(r'\b(\d{1,2})\s*[-–]\s*(\d{1,2})\s*(?:years?|yrs?)\b', description)
    #average for ranges
    if range_match:
        low, high = int(range_match.group(1)), int(range_match.group(2))
        value = (low + high) / 2
    else:
        single_match = re.search(r'\b(\d{1,2})\+?\s*(?:years?|yrs?)\b', description)
        if single_match:
            value = float(single_match.group(1))
        else:
            return None
    return value
df["years_experience"] = df["description"].apply(extract_experience)
#clean locations
df["location"] = df["location"].str.strip()
df[["part1", "part2", "part3"]] = df["location"].str.split(",", expand=True)
df["part1"] = df["part1"].str.strip()
df["part2"] = df["part2"].str.strip()
df["part3"] = df["part3"].str.strip()
df["state"] = df["part2"].fillna(df["part1"])
df.loc[df["state"] == "US", "state"] = None
df.loc[df["state"] == "Remote", "state"] = None
#removes remote jobs from map
df.loc[df["is_remote"] == True, "state"] = None
jobs_per_state = (
    df.groupby("state")
      .size()
      .reset_index(name="job_count")
)
#clean company size
df["company_size"] = df["company_num_employees"].str.replace("employees", "", case=False).str.strip()
def company_size_clean(size):
    if pd.isna(size) or str(size).lower() == "decline to state":
        return None
    #remove commas
    size = str(size).lower().replace(",", "")
    if "-" in size:
        parts = size.split("-")
        low = int(parts[0])
        high = int(parts[1])
        return (low + high) / 2
    if "to" in size:
        parts = size.split(" to ")
        low = int(parts[0].strip())
        high = int(parts[1].strip())
        return (low + high) / 2
    if "+" in size:
        return int(size.replace("+", ""))
    try:
        return int(size)
    except:
        return None
df["company_size_numeric"] = df["company_size"].apply(company_size_clean)


#scatterplot- salary vs years of experience (sample of 5000 rows to fit altair limit, please change if possible)
scatterplot = alt.Chart(df.sample(5000, random_state=42)).mark_point().encode(
    x=alt.X('years_experience:Q', title="Years of Experience"),
    y=alt.Y('mean_salary:Q', title="Mean Salary"),
    tooltip=['title', 'years_experience', 'mean_salary']
).properties(
    width=350,
    height=350
)

boxplot = alt.Chart(df[df['company_num_employees'].notna() &
                       (df['company_num_employees'] != 'Decline to state')].sample(5000, random_state=42)).mark_boxplot(
    size=40,
    ticks=True,
    outliers=True
).encode(
    x=alt.X('company_num_employees:O',
            title='Company Size',
            sort='-y',
            axis=alt.Axis(labelAngle=-30)),  # ← angled labels
    y=alt.Y('mean_salary:Q',
            title='Salary'),
    tooltip=[
        'company_num_employees',
        alt.Tooltip('mean_salary:Q', format='.0f', title='Salary'),
    ]
).properties(
    width=600,
    height=400,
    title='Salary by Company Size'
).configure_title(
    fontSize=16
)

#bar chart- top 10 high paying jobs
top10_salary = df.nlargest(10, 'mean_salary')
top10_salary['title'] = top10_salary['title'].str.title()

bar_chart = alt.Chart(top10_salary).mark_bar().encode(
    x=alt.X(
        'title:N',
        title='Title',
        sort='-y',
        axis=alt.Axis( labelAngle=-30)),
    y=alt.Y('mean_salary:Q',
        title="Mean Salary",
        axis=alt.Axis(format='$,.0f'))
).properties(
    width=350,
    height=350
)

#job distribution map


#salaries per company size

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3("Salary vs Years of Experience"),
            html.Iframe(
                srcDoc=scatterplot.to_html(),
                style={'border-width': '0', 'width': '100%', 'height': '400px'})],
            style={'width': '50%'}),
        html.Div([
            html.H3("Top 10 Jobs by Mean Salary"),
            html.Iframe(
                srcDoc=bar_chart.to_html(),
                style={'border-width': '0', 'width': '100%', 'height': '400px'})],
            style={'width': '50%'})
    ], style={'display': 'flex', 'flexDirection': 'row'}),
    html.Div([
        html.Div([
            html.H3("Salaries per Company Size"),
            html.Iframe(
                srcDoc=boxplot.to_html(),
                style={'border-width': '0', 'width': '100%', 'height': '400px'})],
            style={'width': '50%'})
    ], style={'display': 'flex', 'flexDirection': 'row'})
])

if __name__ == '__main__':
    app.run(debug=True)
