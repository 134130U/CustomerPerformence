import pandas as pd
import numpy as np
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
# import collect
from dash import dash_table as dt
import plotly.express as px
from datetime import date
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
from plotly.subplots import make_subplots
from dash.dash_table.Format import Format, Group
import warnings
warnings.filterwarnings("ignore")

table_header_style = {
    "backgroundColor": "rgb(2,21,70)",
    "color": "white",
    "textAlign": "center",
    'fontSize': 20
}

UPLOAD_DIRECTORY = "Data"
def file_download_link(filename):
    filename = 'finale_data.csv'
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


def update_output():
    """Save uploaded files and regenerate the file list."""
    return [html.Li(file_download_link(filename='finale_data.csv'))]



data = pd.read_csv('Data/finale_data.csv')
tab = data.groupby(['reg_month','ranked_month'])[['total_paid','total_expect_amount']].sum().reset_index()
tab['Ratio %'] = np.round(tab['total_paid']/tab['total_expect_amount']*100,2)
tab=tab.sort_values(by=['reg_month','ranked_month'])


server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])



@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

app.layout = html.Div([
                dcc.Interval(
                                id='interval-component',
                                interval=144000*1000, # in milliseconds
                                n_intervals=0
                        ),
                dbc.Row([
                    dbc.Col([
                        html.A([
                            html.Img(src=app.get_asset_url('oolu.png'),
                                     id='oolu-logo',
                                     style={
                                         "height": "60px",
                                         "width": "auto",
                                         "margin-bottom": "25px",
                                     }, )
                        ]),
                    ],width={'size': 2}),
                    dbc.Col([
                        html.H1('Oolu Customer Performence',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white', "font-family": "Montserrat"
                                }
                                )
                    ],width={'size': 6, 'offset':1}),
                    dbc.Col([
                        html.P(id ='refresh' ,children='Last update  :  ' f'{date.today()}',
                           style={
                                   'textAlign': 'right',
                                   'color': 'orange',
                                   'fontSize': 16}),
                        html.Ul(id="file-list",
                            children=update_output(),
                                style={
                                   'textAlign': 'right',
                                   # 'color': 'orange',
                                   'fontSize': 16}),
                    ],width={'size': 2,'offset':1}),
                ]),
                html.Div(html.Hr()),
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(
                            id = 'pays',
                            multi=True,
                            options=[{'label':x, 'value':x} for x in data['country'].unique()],
                            placeholder="Country",
                            className='form-dropdown',
                            style={'width':'300px', "font-family": "Montserrat"}
                        )
                    ],width={'size': 2}),
                    dbc.Col([
                        dcc.Dropdown(
                            id = 'region',
                            multi=True,
                            options=[{'label':x, 'value':x} for x in data['region'].unique()],
                            placeholder="Region",
                            className='form-dropdown',
                            style={'width':'300px', "font-family": "Montserrat"}
                        )
                    ],width={'size': 2}),
                    dbc.Col([
                        dcc.Dropdown(
                            id = 'prod',
                            multi=True,
                            options=[{'label':x, 'value':x} for x in data['category'].unique()],
                            placeholder="Product",
                            className='form-dropdown',
                            style={'width':'300px', "font-family": "Montserrat"}
                        )
                    ],width={'size': 2}),
                    dbc.Col([
                        dcc.Dropdown(
                            id = 'plan',
                            multi=True,
                            options=[{'label':x, 'value':x} for x in data['payment_type'].unique()],
                            placeholder="Payment Type",
                            className='form-dropdown',
                            style={'width':'300px', "font-family": "Montserrat"}
                        )
                    ],width={'size': 2}),
                    dbc.Col([
                        dcc.Dropdown(
                            id = 'user',
                            multi=True,
                            options=[{'label':x, 'value':x} for x in data['agent'].unique()],
                            placeholder="Agent",
                            className='form-dropdown',
                            style={'width':'300px', "font-family": "Montserrat"}
                        )
                    ],width={'size': 2}),
                    dbc.Col([
                        dcc.Dropdown(
                            id = 'mois',
                            multi=True,
                            options=[{'label':x, 'value':x} for x in sorted(data['reg_month'].unique(),reverse=True)],
                            placeholder="registered Month",
                            className='form-dropdown',
                            style={'width':'300px', "font-family": "Montserrat"}
                        )
                    ],width={'size': 2})
                ]),
                html.Br(),
                dbc.Row([
                    html.Div([
                        dbc.Col([
                            html.Br(),
                            html.H4(children='Collection Rate: Revenues vs expectation over the Months',style={ 'textAlign': 'center','color': 'white'}),

                            dt.DataTable(
                                id='table1',
                                # data=tab.to_dict('records'),
                                style_header=table_header_style,
                                columns=[dict(id=i, name=i,type='numeric', format=Format().group(True)) for i in tab.columns],
                                # style_table={'height': '600px', 'overflowY': 'auto'}
                                style_table={'height': '550px', 'overflowY': 'auto', "font-family": "Montserrat"},
                                fixed_rows={'headers': False},
                                style_cell={'minWidth': '0px', 'maxWidth': '250px', 'black': '100px', 'fontSize': 12,
                                            'backgroundColor': 'with', 'color': 'black',
                                            'textAlign': 'center', "font-family": "Montserrat"},
                                export_format="csv",),
                        ],width={'size': 12, 'offset':0}),

                    ], className="card_container twelve columns")
                ]),
                html.Div(
                    id='update-connection'
                )

            ])
@app.callback(
    [Output('region','options'),
     Output('prod','options'),
     Output('user','options')],
    Input('pays','value')
)

def update_prod(c):
    if c:
        return [{'label':x, 'value':x} for x in data[data['country'].isin(c)]['region'].unique()],[{'label':x, 'value':x} for x in data[data['country'].isin(c)]['category'].unique()],[{'label':x, 'value':x} for x in data[data['country'].isin(c)]['agent'].unique()]
    else:
        return [{'label':x, 'value':x} for x in data['region'].unique()],[{'label':x, 'value':x} for x in data['category'].unique()],[{'label':x, 'value':x} for x in data['agent'].unique()]
@app.callback(
    Output('table1','data'),
    [Input('pays','value'),
     Input('region','value'),
     Input('prod','value'),
     Input('plan','value'),
     Input('user','value'),
     Input('mois','value')]
)


def update_table(c,r,p,i,u,m):
    if not c and not r and not p and not i and not u and not m:
        tab1 = data.groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and not r and not p and not i and not u and not m:
        tab1 = data[data['country'].isin(c)].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and r and not p and not i and not u and not m:
        tab1 = data[(data['country'].isin(c))&(data['region'].isin(r))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and not r and p and not i and not u and not m:
        tab1 = data[(data['country'].isin(c))&(data['category'].isin(p))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and not r and not p and i and not u and not m:
        tab1 = data[(data['country'].isin(c))&(data['payment_type'].isin(i))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and not r and not p and not i and u and not m:
        tab1 = data[(data['country'].isin(c))&(data['agent'].isin(u))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and not r and not p and not i and not u and m:
        tab1 = data[(data['country'].isin(c))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and r and p and not i and not u and not m:
        tab1 = data[(data['country'].isin(c))&(data['region'].isin(r))&(data['category'].isin(p))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and r and not p and i and not u and not m:
        tab1 = data[(data['country'].isin(c))&(data['region'].isin(r))&(data['payment_type'].isin(i))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and r and not p and not i and u and not m:
        tab1 = data[(data['country'].isin(c))&(data['region'].isin(r))&(data['agent'].isin(u))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and r and not p and not i and not u and m:
        tab1 = data[(data['country'].isin(c))&(data['region'].isin(r))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and r and p and i and not u and not m:
        tab1 = data[(data['country'].isin(c))&(data['region'].isin(r))&(data['category'].isin(p))&(data['payment_type'].isin(i))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and r and p and not i and u and not m:
        tab1 = data[(data['country'].isin(c))&(data['region'].isin(r))&(data['category'].isin(p))&(data['agent'].isin(u))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and r and p and not i and not u and m:
        tab1 = data[(data['country'].isin(c))&(data['region'].isin(r))&(data['category'].isin(p))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and r and p and i and u and not m:
        tab1 = data[(data['country'].isin(c))&(data['region'].isin(r))&(data['category'].isin(p))&(data['payment_type'].isin(i))&(data['agent'].isin(u))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and r and p and i and not u and m:
        tab1 = data[(data['country'].isin(c))&(data['region'].isin(r))&(data['category'].isin(p))&(data['payment_type'].isin(i))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if c and r and p and i and u and m:
        tab1 = data[(data['country'].isin(c))&(data['region'].isin(r))&(data['category'].isin(p))&(data['payment_type'].isin(i))&(data['agent'].isin(u))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and r and not p and not i and not u and not m:
        tab1 = data[data['region'].isin(r)].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and r and p and i and u and m:
        tab1 = data[(data['region'].isin(r))&(data['category'].isin(p))&(data['payment_type'].isin(i))&(data['agent'].isin(u))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and r and not p and i and u and m:
        tab1 = data[(data['region'].isin(r))&(data['payment_type'].isin(i))&(data['agent'].isin(u))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and r and not p and not i and u and m:
        tab1 = data[(data['region'].isin(r))&(data['agent'].isin(u))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and r and not p and not i and not u and m:
        tab1 = data[(data['region'].isin(r))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and r and p and not i and not u and not m:
        tab1 = data[(data['region'].isin(r))&(data['category'].isin(p))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and r and p and i and not u and not m:
        tab1 = data[(data['region'].isin(r))&(data['category'].isin(p))&(data['payment_type'].isin(i))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and r and p and not i and u and not m:
        tab1 = data[(data['region'].isin(r))&(data['category'].isin(p))&(data['agent'].isin(u))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and r and p and not i and not u and m:
        tab1 = data[(data['region'].isin(r))&(data['category'].isin(p))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and r and p and i and u and not m:
        tab1 = data[(data['region'].isin(r))&(data['category'].isin(p))&(data['payment_type'].isin(i))&(data['agent'].isin(u))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and r and p and i and not u and m:
        tab1 = data[(data['region'].isin(r))&(data['category'].isin(p))&(data['payment_type'].isin(i))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and not r and p and i and not u and not m:
        tab1 = data[(data['category'].isin(p))&(data['payment_type'].isin(i))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and not r and p and i and u and not m:
        tab1 = data[(data['category'].isin(p))&(data['payment_type'].isin(i))&(data['agent'].isin(u))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and not r and p and i and not u and m:
        tab1 = data[(data['category'].isin(p))&(data['payment_type'].isin(i))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and not r and p and i and u and m:
        tab1 = data[(data['category'].isin(p))&(data['payment_type'].isin(i))&(data['agent'].isin(u))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and not r and not p and i and u and m:
        tab1 = data[(data['payment_type'].isin(i))&(data['agent'].isin(u))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and not r and not p and not i and u and m:
        tab1 = data[(data['agent'].isin(u))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and not r and not p and i and not u and m:
        tab1 = data[(data['payment_type'].isin(i))&(data['reg_month'].isin(m))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and not r and not p and i and u and not m:
        tab1 = data[(data['payment_type'].isin(i))&(data['agent'].isin(u))].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and not r and p and not i and not u and not m:
        tab1 = data[data['category'].isin(p)].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and not r and not p and i and not u and not m:
        tab1 = data[data['payment_type'].isin(i)].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and not r and not p and not i and u and not m:
        tab1 = data[data['agent'].isin(u)].groupby(['reg_month', 'ranked_month'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
    if not c and not r and not p and not i and not u and m:
        tab1 = data[data['reg_month'].isin(m)].groupby(['reg_month', 'ranked_month', 'month_index'])[
            ['total_paid', 'total_expect_amount']].sum().reset_index()
        tab1['Ratio %'] = np.round(tab1['total_paid'] / tab1['total_expect_amount'] * 100, 2)
        tab1 = tab1.sort_values(by=['reg_month', 'ranked_month'])
        return tab1.to_dict('records')
@app.callback(
    Output('refresh', 'children'),
    Input('interval-component', 'n_intervals'))
def update(n):
    if n>0:
        data = pd.read_csv('Data/finale_data.csv')
        tab = data.groupby(['reg_month', 'ranked_month'])[['total_paid', 'total_expect_amount']].sum().reset_index()
        tab['Ratio %'] = np.round(tab['total_paid'] / tab['total_expect_amount'] * 100, 2)
        tab = tab.sort_values(by=['reg_month', 'ranked_month'])
        return ''

if __name__ == "__main__":
    app.run_server(debug=True,dev_tools_ui=False, host='0.0.0.0', port=8060)



