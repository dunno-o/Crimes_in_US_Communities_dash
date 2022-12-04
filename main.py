from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('crimedata_cleaned.csv')

app = Dash(__name__) # Строим дашик (знакомый синтаксис, не правда ли?)

app.layout = html.Div([html.Div([dcc.Dropdown(options={'PolicBudgPerPop': 'Police Budget', 'pctUrban' :
    'Percent of Urban citizens', 'num_of_NotHSGrad' : 'Number of not HS Grad',  'NumImmig' : 'Number of Immigrants',
     "pctUnemployed": "Percentage Unemployed", "population": "Population"}, value="population", id="category")],
        style={'width': '50%', 'display': 'inline-block'}),

html.Div([dcc.Graph(id='graph2'), html.Div('Choose Police Budget Per Population')]),
    dcc.Slider(id='slider', min=df['PolicBudgPerPop'].min(), max=df['PolicBudgPerPop'].max(), step=100000),

    html.Div('Choose Urban Percentage'), dcc.Slider(id='pcturban', min=df['pctUrban'].min(),
    max=df['pctUrban'].max(), step=2),

    html.Div('Choose number of not High school Grad'), dcc.Slider(id='num_of_NotHSGrad', min=df['num_of_NotHSGrad'].min(),
                                                                           max=df['num_of_NotHSGrad'].max(), step=2000000),

    html.Div('Choose number of Immigrants'), dcc.Slider(id='NumImmig', min=df['NumImmig'].min(),
                                                                       max=df['NumImmig'].max(), step=20000),

    html.Div('Choose number of population'), dcc.Slider(id='population', min=df['population'].min(),
                                                                 max=df['population'].max(), step=100000)])


@app.callback(Output('graph2', 'figure'), Input('category', 'value'), Input('slider', 'value'), Input('pcturban', 'value'),
 Input('num_of_NotHSGrad', 'value'), Input('NumImmig', 'value'), Input('population', 'value'))
def update_graph(category, PolicBudgPerPop, pcturban, num_of_NotHSGrad, NumImmig, population):
    dff = df[df['PolicBudgPerPop'].apply(int) <= int(PolicBudgPerPop)]
    dff = dff[dff['pctUrban'] <= pcturban]
    dff = dff[dff['num_of_NotHSGrad'] <= num_of_NotHSGrad]
    dff = dff[dff['NumImmig'] <= NumImmig]
    dff = dff[dff['population'] <= population]

    fig = px.area(dff, x="population", y=["murders", "rapes", "robberies", "assaults", "burglaries", "larcenies", "autoTheft",
    "arsons"])

    fig.update_layout(xaxis_title="Population",
    yaxis_title="Number of crimes", title='Number of crimes by population')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
#%%
