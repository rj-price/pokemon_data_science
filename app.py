import sqlite3
import dash
from dash import dcc
from dash import html
import plotly.express as px

# Create a connection to the SQLite database
conn = sqlite3.connect('pokemon.db')

# Define the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1('Pokémon Dashboard'),
    dcc.Dropdown(
        id='generation-dropdown',
        options=[
            {'label': 'Generation 1', 'value': 1},
            {'label': 'Generation 2', 'value': 2},
            {'label': 'Generation 3', 'value': 3},
            {'label': 'Generation 4', 'value': 4},
            {'label': 'Generation 5', 'value': 5},
            {'label': 'Generation 6', 'value': 6},
            {'label': 'Generation 7', 'value': 7},
            {'label': 'Generation 8', 'value': 8},
        ],
        value=1,
        placeholder='Select a generation'
    ),
    dcc.Graph(
        id='type-counts',
        figure={}
    )
])

# Define the callbacks
@app.callback(
    dash.dependencies.Output('type-counts', 'figure'),
    [dash.dependencies.Input('generation-dropdown', 'value')])
def update_type_counts(generation):
    query = f'''
    SELECT type1, COUNT(*) AS count
    FROM pokemon
    WHERE generation = {generation}
    GROUP BY type1
    '''
    df = pd.read_sql_query(query, conn)
    fig = px.bar(df, x='type1', y='count')
    fig.update_layout(
        title=f'Distribution of Pokémon Types in Generation {generation}',
        xaxis_title='Type',
        yaxis_title='Count'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)