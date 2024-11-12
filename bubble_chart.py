import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# Bubble Chart Resource - https://plotly.com/python/bubble-charts/

def cleaning_df():
    episodes_df = pd.read_csv('friends_episodes.csv')
    episodes_df['Episode_Title'] = episodes_df['Episode_Title'].astype('string')
    episodes_df['Summary'] = episodes_df['Summary'].astype('string')
    episodes_df['Director'] = episodes_df['Director'].astype('string')
    print(episodes_df.columns)
    return episodes_df

friends_df = cleaning_df()


app = Dash(__name__)

app.layout = html.Div([
    html.H4('TV Show Ratings'),

    # Define Layout
    dcc.Graph(id="FriendsBubbleChart"),
    html.P("Star Slider"),
    dcc.RangeSlider(min=6, max=10, value=[8, 9], id='RatingSlider',)
])

@app.callback(
    Output("FriendsBubbleChart", "figure"),
    [Input("RatingSlider", "value")]

)

def bubble_chart(Rating):
    print(Rating)
    Slider_df = friends_df[(friends_df['Stars']>Rating[0]) & (friends_df['Stars'] < Rating[1])]


    fig = px.scatter(Slider_df, x="Stars", y="Votes", size="Stars", color="Season", hover_name="Summary", hover_data=["Episode_Title", "Duration"],log_x=True,
                     size_max=60)
    #fig.show()

    return fig

app.run(debug=True)
'''
hover_text = []
bubble_size = []

for index, row in episodes_df.iterrows():
    hover_text.append(('Episode Title: {EpisodeTitle}<br>' +
                       'Season: {Season}<br>' +
                       'Rating: {Stars}<br>' +
                       'Episode Summary: {Summary}<br>').format(EpisodeTitle=row['Episode_Title'],
                                                                Season=row['Season'],
                                                                Stars=row['Stars'],
                                                                Summary=row['Summary']))
    bubble_size.append(math.sqrt(row['Stars']))

episodes_df['Text'] = hover_text
episodes_df['Size'] = bubble_size
print('Type', type(episodes_df['Size']))
sizeref = 2.*max(episodes_df['Size'])/(100**2)

season_count = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
season_data = {Season:episodes_df.query("Season == '%s'" %Season)
               for Season in season_count}

fig = go.Figure()

for S_count, Season in season_data.items():
    fig.add_trace(go.Scatter(
        x=Season['Stars'], y=Season['Votes'],
        name=S_count, text=Season['Text'],
        #marker_size=S_count['Size'],
    ))

fig.update_traces(mode='markers', marker=dict(sizemode='area', sizeref=sizeref, line_width=2))

fig.update_layout(
title='Friends Episode Ratings',
    xaxis=dict(
        title='Stars',
        gridcolor='white',
        type='log',
        gridwidth=2,
    ),
    yaxis=dict(
        title='Votes for Each Episode',
        gridcolor='white',
        gridwidth=2,
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
)
fig.show()
'''


