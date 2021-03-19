import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


oil = pd.read_csv('oil.csv', delimiter=';')
oil['DATE'] = pd.to_datetime(oil['DATE'])
surf = pd.read_csv('surf.csv', delimiter=';')
df = oil.merge(surf, how='left', on='WellID')
df.iloc[30000:40000,5].fillna(0, inplace=True)
df = df.iloc[30000:40000,:]

app = dash.Dash(__name__)

server = app.server

fig1 = px.scatter(
        df, x="SURFX", y="SURFY",
        color='FORMATION', size='POILRATE',
        animation_frame=df['DATE'].astype(str), hover_data=['WellID'],
        animation_group='WellID', size_max=20,
        range_x=[548000, 572000], range_y=[3588000, 3601000])

fig2 = px.line(df[df['WellID'] == 'AD2-10-3H'], x="DATE", y="POILRATE", title='AD2-10-3H', range_y=[0, 5000])


app.layout = html.Div([
    html.H1('Oil field production Dashboard'),
    html.Div([dcc.Graph(id="map", figure=fig1)], style={'display': 'inline-block', 'width': '50%'}),
    html.Div([dcc.Graph(id="prod_plot", figure=fig2)], style={'display': 'inline-block', 'width': '50%'})
])


@app.callback(
    Output("prod_plot", "figure"),
    [Input("map", "clickData")])
def update_plot(clickData):
    Well = clickData['points'][0]['id']
    df_filtered = df[df['WellID'] == Well]
    fig2 = px.line(df_filtered, x="DATE", y="POILRATE", title=Well, range_y=[0, 5000])
    return fig2

if __name__ == '__main__':
    app.run_server()



