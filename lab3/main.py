import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
import numpy as np

app = dash.Dash(
    __name__,
    # 从国内可顺畅访问的cdn获取所需的原生bootstrap对应css
    external_stylesheets=['https://cdn.staticfile.org/twitter-bootstrap/4.5.2/css/bootstrap.min.css']
)

df = pd.read_csv('test.csv')

df_new = pd.read_csv('dataset/black-friday/BlackFriday.csv')


available_indicators = df['Indicator Name'].unique()

city_category = df_new['City_Category'].unique()

Occupation = df_new['Occupation'].unique()

#用户画像的初始选择框值
city_category_value = 'A'
occupation = 1

app.layout = html.Div([
    html.Div([
        dbc.Container([
            dbc.Row(
            [
                html.Img(src='https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/clip-lettering-big-data (1).png',style={'width':'30%'}),
                html.H1('Black Friday DashBoard!',style={'margin-top':'3%'}),
             ]),
            html.P('1853572 QiaoLiang',style={'margin-left':'30%'})
            ]

        ),

    html.Div([
        html.H2('User Profile'),
    ]),
    html.Div([
        html.P('city category'),
        dcc.Dropdown(
            id='city_category',
            options=[
                {'label': item, 'value': item}
                for item in city_category
            ],
            value= city_category_value
        ),
    ],
        style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        html.P('occupation'),
        dcc.Dropdown(
            id='Occupation',
            options=[
                {'label': item, 'value': item}
                for item in Occupation
            ],
            value= occupation
        ),
    ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),

    # 饼状图
    html.Div([
       dcc.Graph(
           id='user-profile-scatter',
       )
    ],style={'width': '49%', 'display': 'inline-block', 'padding': '0 20','box-shadow': 'rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;'}),

    #散点图
    html.Div([
        dcc.Graph(
            id='shopping-cart-distribution',
           # hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

    # 柱状图
    html.Div([
        dcc.Graph(
            id='purchase-age',
            # hoverData={'points': [{'customdata': 'Japan'}]}
        figure={
            'data':[
                {'x':[4,6,8],'y':[12,16,18],'type':'bar','name':'chart one'},
                {'x':[4,6,8],'y':[20,24,28],'type':'bar','name':'chart two'}
            ],
            'layout':{
                'title':'simple bar chart',
            }
        }
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

        # 饼状图
        html.Div([
            dcc.Graph(
                id='gender-bar',
            )
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20',
                  'box-shadow': 'rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;'}),

    # 源数据
    html.Div([
        html.H1('Part of source data'),
        dash_table.DataTable(
            id='dash_table',
            data = df_new[(df_new['City_Category'] == 'A') & (df_new['Occupation'] == 1)].to_dict('records'),
            columns=[
                {'name': column, 'id': column}
                for column in df_new.columns
            ],
            page_size=15,
            style_header={
                'font-family': 'Times New Roman',
                'font-weight': 'bold',
                'text-align': 'center',
            },
            style_data={
                'font-family': 'Times New Roman',
                'text-align': 'center'
            },
            sort_action='native'
        )
    ],style={'width':'80%','margin-left':'5%'}),
])
    ])

@app.callback(
    dash.dependencies.Output('purchase-age','figure'),
    [dash.dependencies.Input('city_category', 'value'),
     dash.dependencies.Input('Occupation', 'value')]
)
def create_bar_age(city_category, Occupation):
    dff = df_new[(df_new['City_Category'] == city_category) & (df_new['Occupation'] == Occupation)]
    age =[]
    purchase=[]
    grouped_age = dff.groupby('Age')
    for name,group in grouped_age:
        age.append(name)
        purchase.append(group['Purchase'].sum())
    return {
        'data':[
            {'x': age, 'y': purchase, 'type': 'bar', 'name': 'chart one'},
        ],
        'layout': {
            'height': 300,
            'width':500,
            'margin': {'l': 40, 'b': 30, 'r': 10, 't': 30},
            'title':'Total shopping by age group in city '+ str(city_category)
        }
            }

@app.callback(
    dash.dependencies.Output('shopping-cart-distribution','figure'),
    [dash.dependencies.Input('city_category', 'value'),
     dash.dependencies.Input('Occupation', 'value')]
)
def create_time_series_shopping(city_category, Occupation):
    dff = df_new[(df_new['City_Category'] == city_category) & (df_new['Occupation'] == Occupation)]
    grouped = dff.groupby('Product_ID')
    data = []
    for name, group in grouped:
        data.append([name, len(group)])
    columns = ['User_ID', 'number']
    shopping_data = pd.DataFrame(data, columns=columns)
    grouped = shopping_data.groupby('number')
    num_cart = []
    people_num = []
    for name, group in grouped:
        num_cart.append(name)
        people_num.append(len(group))
    return {
        'data': [go.Scatter(
            x= people_num,
            y= num_cart,
            # text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            # customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
            }
        )],
        'layout': go.Layout(
            title='Number of users with different number of shopping carts in city '+ str(city_category)+' with occupation'+ str(Occupation),
            xaxis={
                'title': 'shopping cart number',
                'type': 'linear'
            },
            yaxis={
                'title': 'number of people',
                'type': 'linear'
            },
            margin={'l': 40, 'b': 30, 't': 40, 'r': 0},
            height=400,
            width=800,
            hovermode='closest',
        )
    }


@app.callback(
    dash.dependencies.Output('dash_table','data'),
    [dash.dependencies.Input('city_category','value'),
     dash.dependencies.Input('Occupation','value')]
)
def update_dash_table(city_category,Occupation):
    return  df_new[(df_new['City_Category'] == city_category) & (df_new['Occupation'] == Occupation)].to_dict('records')

@app.callback(dash.dependencies.Output('user-profile-scatter', 'figure'),
              [dash.dependencies.Input('city_category','value'),
                dash.dependencies.Input('Occupation','value')])
def create_time_series_one(city_category, Occupation):
    dff = df_new[(df_new['City_Category'] == city_category) & (df_new['Occupation'] == Occupation)]
    grouped = dff.groupby(['Age'])
    age_group = []
    num = []
    for name, group in grouped:
        age_group.append(name)
        grouped_new = group.groupby(['User_ID'])
        number = 0
        for name1, group1 in grouped_new:
            print(name1)
            number += 1
        num.append(number)
    return {
        'data':[
            {'labels':age_group,'values':num,'type':'pie','name':'饼图','hole': '0.8','size':'100'}
        ],
        'layout': {
            'height': 300,
            'width':600,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 30},
            'title':'Age distribution of users in city '+ str(city_category)+' with occupation'+ str(Occupation)
        }
            }

@app.callback(dash.dependencies.Output('gender-bar', 'figure'),
              [dash.dependencies.Input('city_category','value'),
                dash.dependencies.Input('Occupation','value')])
def create_gender_bar(city_category, Occupation):
    dff = df_new[(df_new['City_Category'] == city_category) & (df_new['Occupation'] == Occupation)]
    bf_gen_mar = dff.groupby(['Gender', 'Marital_Status'])
    # bf_gen = dff.groupby(['Gender']).count()
    name_list = []
    purchase = []
    for name, group in bf_gen_mar:
        name_str = ''
        if name[0] == 'F':
            name_str += 'Female '
        else:
            name_str += 'Male '
        if name[1] == 0:
            name_str += 'not married'
        else:
            name_str += 'married'
        name_list.append(name_str)
        purchase.append(group['Purchase'].sum())
    return {
        'data':[
            {'labels':name_list,'values':purchase,'type':'pie','name':'饼图','size':'200'}
        ],
        'layout': {
            'height': 300,
            'width':800,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 30},
            'title':'Purchasing power by gender and marital status in city '+ str(city_category)+' with occupation'+ str(Occupation)
        }
            }



if __name__ == '__main__':
    app.run_server(debug= True)