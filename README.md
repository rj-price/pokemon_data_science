# Exploratory Data Analysis on Pokémon

## Objective
The objective of this project is to perform exploratory data analysis on a dataset containing information about Pokémon, using Python and SQL. The dataset will be analyzed to gain insights into various attributes of Pokémon and their relationships.

## Dataset
The dataset to be used in this project can be found at https://www.kaggle.com/rounakbanik/pokemon. The dataset contains information on 802 Pokémon, including their name, type, abilities, stats, and more.

## Tasks

### Step 1: Load the dataset into a SQL database
First, we need to load the dataset into a SQL database. We can use SQLite for this project as it is lightweight and doesn't require a separate database server to be installed.
```
import sqlite3
import pandas as pd

# Load the dataset into a pandas dataframe
df = pd.read_csv('pokemon.csv')

# Create a connection to the SQLite database
conn = sqlite3.connect('pokemon.db')

# Write the dataframe to a SQL table
df.to_sql('pokemon', conn, if_exists='replace', index=False)
```

### Step 2: Write SQL queries for basic data cleaning and exploration
Next, we will write SQL queries to perform some basic data cleaning and exploration. For example, we can check for missing values and remove duplicates.
```
# Check for missing values
query = '''
SELECT *
FROM pokemon
WHERE name IS NULL OR type1 IS NULL OR type2 IS NULL OR hp IS NULL OR attack IS NULL
'''
null_values = pd.read_sql_query(query, conn)
print(f'The number of null values in the dataset is {len(null_values)}')

# Remove duplicates
query = '''
SELECT DISTINCT *
FROM pokemon
'''
df = pd.read_sql_query(query, conn)
```

### Step 3: Use Python to visualize the data
Now, we will use Python to visualize the data and gain insights into various attributes of Pokémon. For example, we can create a bar chart showing the distribution of Pokémon types.
```
import matplotlib.pyplot as plt

# Count the number of Pokémon for each type
query = '''
SELECT type1, COUNT(*) AS count
FROM pokemon
GROUP BY type1
'''
df_type_counts = pd.read_sql_query(query, conn)

# Create a bar chart of the type counts
plt.bar(df_type_counts['type1'], df_type_counts['count'])
plt.xticks(rotation=90)
plt.xlabel('Type')
plt.ylabel('Count')
plt.title('Distribution of Pokémon Types')
plt.show()
```
We can also create a scatter plot showing the relationship between a Pokémon's attack and defense stats.
```
import seaborn as sns

sns.scatterplot(data=df, x='attack', y='defense', hue='type1')
plt.title('Relationship between Attack and Defense Stats')
plt.show()
```

### Step 4: Use SQL to perform more advanced queries
We can use SQL to perform more advanced queries on the data. For example, we can find the top 10 Pokémon by total stat points.
```
# Calculate the total stat points for each Pokémon
query = '''
SELECT name, (hp + attack + defense + sp_atk + sp_def + speed) AS total_stats
FROM pokemon
'''
df_stats = pd.read_sql_query(query, conn)

# Sort by total stat points and select the top 10
df_stats = df_stats.sort_values(by='total_stats', ascending=False).head(10)
print(df_stats)
```
We can also find the most common type combinations.
```
# Count the number of Pokémon for each type combination
query = '''
SELECT type1, type2, COUNT(*) AS count
FROM pokemon
GROUP BY type1, type2
ORDER BY count DESC
LIMIT 10
'''
df_type_combinations = pd.read_sql_query(query, conn)
print(df_type_combinations)
```

### Step 5: Create a dashboard or interactive visualization
Dash is a Python framework for building web applications that are powered by Plotly visualizations. We can use it to create an interactive dashboard that allows the user to explore the data in more depth. Here's an example dashboard that shows the distribution of Pokémon by type and allows the user to filter by generation:
```
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import sqlite3

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
```
In this example, we first import the necessary libraries and create a connection to the SQLite database. We then define the layout of the dashboard using the html.Div and dcc components provided by Dash. The dcc.Dropdown component allows the user to select a generation, and the dcc.Graph component displays the distribution of Pokémon types for the selected generation.

We define a callback function using the @app.callback decorator. This function takes the selected generation as an input and returns a Plotly bar chart of the distribution of Pokémon types for that generation. The dash.dependencies.Output and dash.dependencies.Input decorators are used to specify the inputs and outputs of the callback function.

Finally, we run the app using the app.run_server() method.

To run this example, save the code to a file named app.py and run python app.py in the terminal. Then, open a web browser and go to http://127.0.0.1:8050/ to view the dashboard.

## Deliverables
The deliverables for this project could include:
 * A Jupyter notebook or Python script containing the code used for data cleaning, exploration, and visualization.
 * A SQL script containing the queries used to extract and analyze the data.
 * A dashboard or interactive visualization that allows the user to explore the data in more depth.