# Import requ # Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard',
    style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    # dcc.Dropdown(id='site-dropdown',...) html.Br(),
    dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
            ],
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True
    ),
    html.Br(),
    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    # TASK 3: Add a slider to select payload range
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                value=[min_payload, max_payload]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ])    #closed layout

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site): # add 1 parameters here, entered_site (1 input)
    if entered_site == 'ALL':
        site_counts = spacex_df[spacex_df['class'] == 1]['Launch Site'].value_counts().reset_index() #successfull launch
        site_counts.columns = ['Launch Site', 'count']
        fig = px.pie(site_counts, values='count', 
        names='Launch Site', 
        title='Total Success Launches by Site') #USE FILTERED DF CALLED SITECOUNTS
        return fig
    else: # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        fig = px.pie(success_counts, values='count', names='class', 
        title=f'Total Success Launches for site {entered_site}')
        return fig
    

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_range):
    # Filtrar los datos por el rango de payload seleccionado
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                             (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color="Booster Version Category",
                         title='Correlation between Payload and Success for all Sites')
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class', 
                         color="Booster Version Category",
                         title=f'Correlation between Payload and Success for {entered_site}')

    return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
    #app.run_server(debug=True, port=8054) #port can be change if you need