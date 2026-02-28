import dash
from dash import html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import textwrap
import os

alt.data_transformers.disable_max_rows()

base_path = os.path.dirname(__file__)
data_path = os.path.join(base_path, "..", "data", "cleaned", "ds_jobs.csv")
df = pd.read_csv(data_path)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#company size cal
min_size = int(df['company_size_numeric'].min())
max_size = int(df['company_size_numeric'].max())
slider_marks = {}
for i in range(0, max_size + 1, 10000):
    if i > 0:
        k_value = i // 1000
        slider_marks[i] = str(k_value) + "k"
    else:
        slider_marks[i] = "1"

#filters 
sidebar = dbc.Col([
    html.H5("Filters", className="pt-3 text-primary"),
    html.Hr(),
    #filter1
    html.Label("Company Size", className="small font-weight-bold"),
    dcc.RangeSlider(id='company-slider', min=min_size, max=max_size, step=500,value=[min_size, max_size],marks=slider_marks),
    #filter2
    html.Label("Job Titles (Select Multiple)", className="mt-4 small font-weight-bold"),
    dbc.Button("Select All", id="select-all-btn", n_clicks=0, size="sm", color="link", className="p-0 mb-1"),
    dcc.Input(id='search-box', type='text', placeholder='Search...', className="mb-2 w-100 form-control-sm"), 
    html.Div([dcc.Checklist(id='job-title-checklist',options=[{'label': i, 'value': i} for i in sorted(df['job_type'].unique())], value=['Data Scientist'],labelStyle={'display': 'block', 'fontSize': '11px', 'margin-bottom': '5px'}),], style={'height': '25vh', 'overflowY': 'auto', 'border': '1px solid #dee2e6', 'padding': '10px', 'backgroundColor': 'white'}),
    #filter3
    html.Label("Experience Level", className="mt-4 small font-weight-bold"),
    dcc.RadioItems(id='exp-radio',options=[{'label': 'Entry-Level', 'value': 'Entry-Level'}, {'label': 'Mid-Level', 'value': 'Mid-Level'},{'label': 'Senior-Level', 'value': 'Senior-Level'},{'label': 'Executive-Level', 'value': 'Executive-Level'}],value='Entry-Level', labelStyle={'display': 'block', 'fontSize': '12px'}),], width=2, style={'height': '100vh', 'backgroundColor': '#f8f9fa', 'borderRight': '1px solid #dee2e6', 'padding': '20px'})

content = dbc.Col([
    #row 1 30% height
    dbc.Row([dbc.Col([html.Div(id='static-bar-container', style={'height': '30vh'})], width=12)], className="g-0"),
    #row 2 35% height
    dbc.Row([dbc.Col([html.Div(id='scatter-container', style={'height': '35vh'})], width=6),dbc.Col([dcc.Graph(id='job-map', style={'height': '35vh'}, config={'displayModeBar': False})], width=6),], className="g-0"),
    #row 3 35% height 
    dbc.Row([dbc.Col([html.Div(id='box-container', style={'height': '35vh'})], width=12)], className="g-0")], width=10, style={'height': '100vh', 'overflow': 'hidden', 'padding': '5px'})

app.layout = dbc.Container([
    dbc.Row([dbc.Col(html.H2("Data Science Job Market Dashboard", className="text-center py-3 text-white bg-primary mb-0"), width=12)], className="g-0"),
    dbc.Row([sidebar, content], className="g-0")], fluid=True, style={'height': '100vh', 'overflow': 'hidden'})

@app.callback(
    [Output('static-bar-container', 'children'),
     Output('scatter-container', 'children'),
     Output('box-container', 'children'),
     Output('job-map', 'figure')],
    [Input('job-title-checklist', 'value'),  
     Input('company-slider', 'value'),
     Input('exp-radio', 'value')]
)
def update_dashboard(selected_job, size_range, selected_exp):
    #bar chart- top 10 high paying jobs
    filtered_df = df[(df['job_type'].isin(selected_job)) & 
                 (df['company_size_numeric'] >= size_range[0]) & 
                 (df['company_size_numeric'] <= size_range[1]) &
                 (df['experience_level'] == selected_exp)]

    top10_type_df = df.groupby('job_type')['mean_salary'].mean().nlargest(10).reset_index()
    top10_type_df['job_type'] = top10_type_df['job_type'].str.title()
    
    top10_type_df['type_wrapped'] = top10_type_df['job_type'].apply(lambda x: textwrap.wrap(x, width=20)[:3])
    
    bar = alt.Chart(top10_type_df).mark_bar(color='#4c78a8').encode(x=alt.X('type_wrapped:N', sort='-y', title=None, axis=alt.Axis(labelAngle=0, labelPadding=20)),
        y=alt.Y('mean_salary:Q', title="Average Mean Salary", axis=alt.Axis(format='$,.0f')),tooltip=['job_type', alt.Tooltip('mean_salary:Q', format='$,.0f')]).properties( width='container', height=200, title="Top 10 High Paying Jobs")

    #scatterplot- salary vs years of experience (sample of 5000 rows to fit altair limit, please change if possible)
    scatter = alt.Chart(filtered_df.sample(min(len(filtered_df), 5000))).mark_point().encode(x=alt.X('years_experience:Q', title="Years of Experience"),
        y=alt.Y('mean_salary:Q', title="Mean Salary"),
    ).properties(width='container', height=200, title="Salary vs Experience")

    # boxplot salary by company size
    box = alt.Chart(filtered_df[filtered_df['company_num_employees'].notna()]).mark_boxplot(size=90,extent='min-max',color='#4c78a8').encode(
        x=alt.X('company_num_employees:O', sort='-y', title='Company Size', axis=alt.Axis(labelAngle=-20)),
        y=alt.Y('mean_salary:Q', title='Salary'),
    ).properties(width='container', height=250, title="Salaries per Company Size")
    
    #map
    map_fig = px.choropleth(
        filtered_df.groupby('state').size().reset_index(name='job_count'),
        locations='state', locationmode='USA-states', color='job_count',
        scope='usa', color_continuous_scale='Blues'
    )
    map_fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_text="Job Distribution")

    return (
        html.Iframe(srcDoc=bar.to_html(), style={'width': '100%', 'height': '100%', 'border': 'none', 'overflow': 'hidden'}),
        html.Iframe(srcDoc=scatter.to_html(), style={'width': '100%', 'height': '100%', 'border': 'none', 'overflow': 'hidden'}),
        html.Iframe(srcDoc=box.to_html(), style={'width': '100%', 'height': '100%', 'border': 'none', 'overflow': 'hidden'}),
        map_fig
    )

@app.callback(
    Output('job-title-checklist', 'value'),
    Input('select-all-btn', 'n_clicks'),
    prevent_initial_call=True
)
def select_all_jobs(n_clicks):
    return sorted(df['job_type'].unique())
    
@app.callback(
    Output('job-title-checklist', 'options'),
    Input('search-box', 'value')
)

def filter_job_titles(search_value):
    all_jobs = df['job_type'].unique()
    all_jobs = sorted(all_jobs)
    
    if search_value == "" or search_value is None:
        results = []
        for job in all_jobs:
            option = {'label': job, 'value': job}
            results.append(option)
        return results
    
    filtered_jobs = []
    for job in all_jobs:
        if search_value.lower() in job.lower():
            filtered_jobs.append(job)
            
    final_list = []
    for job in filtered_jobs:
        final_list.append({'label': job, 'value': job})
        
    return final_list
    
if __name__ == '__main__':
    app.run(debug=True)