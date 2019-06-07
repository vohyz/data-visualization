import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.plotly as py
import pandas as pd
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df = pd.read_csv('lab3-datasets\\black-friday\\BlackFriday.csv')
dfn = pd.read_csv('lab3-datasets\\black-friday\\BlackFriday.csv',nrows=2000)
def count(d):
    a = 0
    b = 0
    for i in d:
        if i == 'M':
            a+= 1
        elif i == 'F':
            b+=1

    return a,b
def countm(d):
    a = 0
    b = 0
    for i in d:
        if i == 'M':
            a+= 1


    return a
def countf(d):
    a = 0
    b = 0
    for i in d:
        if i == 'F':
            a+= 1


    return a
mmn = dfn['Purchase']
trace1 = go.Bar(
    x=dfn['Purchase'],
    y=[countm(dfn[abs(dfn['Purchase']-i)<500]['Gender'])for i in mmn],
    name='F'
)
trace2 = go.Bar(
    x=dfn['Purchase'],
    y=[countf(dfn[abs(dfn['Purchase']-i)<500]['Gender'])for i in mmn],
    name='M'
)

app.layout=html.Div([
dcc.Graph(
        id='Number-Purchase',
        figure={
            'data': [
                trace1,trace2
            ],
            'layout': go.Layout(
                xaxis={'title': 'Purchase'},
                yaxis={'title': 'Number of people'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }

    ),
dcc.Graph(
        id='Age-Purchase-Male',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['Gender'] == i]['Purchase'],
                    y=df[df['Gender'] == i]['Age'].unique(),
                    text=df[df['Gender'] == i]['Gender'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=str(i)
                ) for i in df.Gender.unique()

            ],
            'layout': go.Layout(
                xaxis={'title': 'Purchase'},
                yaxis={'title': 'Age'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    html.Div([html.H1("BlackFirday-Gender-sex-Age")], style={"float": "left"}),
    dcc.Graph(id="my-graph"),
    html.Div([dcc.Slider(id='Age-selected', min=1, max=7, value=1,
                         marks={1: "0-17", 2: "18-25", 3: "26-35",4: "36-45", 5: "46-50", 6: "51-55", 7: "55+"}
                         )],
             style={'textAlign': "center", "margin": "30px", "padding": "10px", "width": "65%", "margin-left": "auto",
                    "margin-right": "auto"}),
], className="container")

name=['0',"0-17", "18-25", "26-35", "36-45", "46-50","51-55", "55+"]
@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("Age-selected", "value")]
)
def update_graph(selected):
    select = name[selected]
    return {
        "data": [go.Pie(labels=df["Gender"].unique().tolist(), values=count(df[df["Age"] == select]["Gender"]),
                        marker={'colors': ['#EF963B', '#C93277', '#349600', '#EF533B', '#57D4F1']}, textinfo='label')],
        "layout": go.Layout(title=f"", margin={"l": 300, "r": 300, },
                            legend={"x": 1, "y": 0.7})}


if __name__ == '__main__':
    app.run_server()