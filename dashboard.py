#load necessary libraries
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
import re

df = pd.read_csv("data/ds_jobs.csv")







#scatterplot- salary vs years of experience (sample of 5000 rows to fit altair limit, please change if possible)
scatterplot = alt.Chart(df.sample(5000, random_state=42)).mark_point().encode(
    x='years_experience',
    y='mean_salary',
    tooltip=['title', 'years_experience', 'mean_salary']
)





# boxplot
# select distinct for company_num_employees
df["company_num_employees"].unique()

df_salary_per_company_size = df[["title", "company_num_employees", "mean_salary", "location"]]

# remove rows with missing values for company_num_employees
df_salary_per_company_size = df_salary_per_company_size.dropna(subset=["company_num_employees"])

# remove rows with "Decline to state" for company_num_employees
df_salary_per_company_size = df_salary_per_company_size[df_salary_per_company_size["company_num_employees"] != "Decline to state"]

# combine "1", "1 to 50", "2 to 10", "11 to 50" into "1 to 50"
df_salary_per_company_size.loc[df_salary_per_company_size["company_num_employees"].isin(["1", "1 to 50", "2 to 10", "11 to 50"]), "company_num_employees"] = "1 to 50"

df_salary_per_company_size["company_num_employees"].unique()

size_order = [
    '1 to 50',
    '51 to 200',
    '201 to 500',
    '501 to 1,000',
    '1,001 to 5,000',
    '5,001 to 10,000',
    '10,000+'
]

df_salary_per_company_size['company_num_employees'] = pd.Categorical(
    df_salary_per_company_size['company_num_employees'],
    categories=size_order,
    ordered=True
)

df_salary_per_company_size = df_salary_per_company_size.sort_values('company_num_employees')

alt.renderers.enable('default')
# alt.data_transformers.enable('vegafusion')

boxplot = alt.Chart(df_salary_per_company_size.sample(5000, random_state=42)).mark_boxplot(
    size=40,
    ticks=True,
    outliers=True
).encode(
    x=alt.X('company_num_employees:O',
            title='Company Size',
            sort=size_order),
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
).configure_axis(
    labelAngle=0
).configure_title(
    fontSize=16
)


# app = dash.Dash(__name__)
# app.layout = html.Div([
#         html.H3("Salary vs Years of Experience"),
#         html.Iframe(
#             srcDoc=scatterplot.to_html(),
#             style={'border-width': '0', 'width': '100%', 'height': '400px'})])


app = dash.Dash(__name__)
app.layout = html.Div([
        html.H3("Salary by Company Size"),
        html.Iframe(
            srcDoc=boxplot.to_html(),
            style={'border-width': '0', 'width': '100%', 'height': '500px'})])




#job distribution map


if __name__ == '__main__':
    app.run(debug=True) 