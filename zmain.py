"""
Name: Aidan Cremins and Ashley Catoggio
MA346: Section 1
Data: Top Spotify Songs and Grammy Awards
"""

# Imports a variety of libraries and use will use the basics such as
# pandas and numpy, but we will also used streamlit in order to crate
# the subsequent dashboard associated with our data analysis.
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# Import all Spotify and Grammy award data from excel files. The .csv file containing information about the top 2000
# songs on Spotify at some point in 2019 is saved to a data frame called "spotify_df". The .csv with information
# about songs that have been nominated for a Grammy Award is saved to a data frame called "grammys_df".
spotify_df = pd.read_csv("Spotify-2000.csv")
grammys_df = pd.read_csv("the_grammy_awards.csv")


# The 'Length (Duration)' column from the Spotify data is classified as an object (essentially a string) instead of
# a numeric variable type, so we converted the data type in the following code.
# Use the .replace() method to remove commas from all values in the column
spotify_df["Length (Duration)"] = spotify_df["Length (Duration)"].replace\
(",","",regex=True)
# Use .astype() to change it to an integer.
spotify_df["Length (Duration)"] = spotify_df["Length (Duration)"].astype\
("int64")


# Create a new column in spotify_df called "id_column" that combines the "Title" and "Year" columns and create a new
# column in grammys_df called "id_column" that combines the "nominee" and "year" columns. Use .map(str) to turn all rows
# of "Year" into strings. We use "+" to combine the two columns which yields our desired ID column for both data frames.
# This is how we will link the Spotify and Grammys data frames.
spotify_df["id_column"] = spotify_df["Title"] + spotify_df["Year"].map(str)
grammys_df["id_column"] = grammys_df["nominee"] + grammys_df["year"].map(str)


# Use np.where() to create a new column called "Grammy" which has a value of 1 if there's a match between the two ID
# columns (meaning the song is Grammy nominated), and a value of 0 if not.
spotify_df["Grammy"] = np.where(spotify_df["id_column"].isin\
                                (grammys_df["id_column"]),1,0)


# Title in main frame
st.title("Spotify Top 2,000 Songs (1956-2019)")
# Title in sidebar with italicized font by using *
st.sidebar.title("*Additional Information*")
# Prints Spotify logo, parameter values at bottom of code
def image(img, description):
    sidebar = st.sidebar.image(img, caption=description)
    return img


# Currently, the "Top Genre" column in the data set is extremely specific with genres like "detroit hip hop", "adult
# standards", and "arkansas country". These categories are far too specific to be of use in a predictive model because
# there's too few songs in each category. Thus, we can create a new "Genre" column that groups songs into broader
# genres. This forms  just 7 genre categories: Dutch, Rock, Country, Pop, Hip Hop/Rap, Indie, and Other. This makes it
# more likely that genre will be a useful predictor in a predictive model.

# Create an empty "Genre" column that will be filled with values below
spotify_df['Genre'] = ""


# Iterate through each row in the data frame and see if certain key phrases are found in the "Top Genre" column. If so,
# set the new "Genre" name according to the if and elif statements. If no key phrases are found, list "Genre" as being
# the generic 'Other'.
for index, row in spotify_df.iterrows():
    if "dutch" in row["Top Genre"]:
        row["Genre"] = "Dutch"
    elif "rock" in row["Top Genre"] or "british invasion" in row["Top Genre"] \
    or "adult standards" in row["Top Genre"] or "metal" in row["Top Genre"]:
        row["Genre"] = "Rock"
    elif "country" in row["Top Genre"]:
        row ["Genre"] = "Country"
    elif "pop" in row["Top Genre"] or "british soul" in row["Top Genre"]:
        row["Genre"] = "Pop"
    elif "hip hop" in row["Top Genre"] or "rap" in row["Top Genre"]:
        row["Genre"] = "Hip Hop/Rap"
    elif "indie" in row["Top Genre"] or "permanent wave" in row["Top Genre"] \
        in row["Top Genre"]:
        row["Genre"] = "Indie"
    else:
        row["Genre"] = "Other"
    # Sets genre value for each particular row
    spotify_df["Genre"].loc[index] = row["Genre"]


# Creates a bar chart in order to show the user the top genres, based on the overall genres that were created above.
# Utilizing matplotlib.pyplot allowed us to add axis labels in order to make the chart easier to read for the viewer.
# The bar chart can be seen by clicking a button in the sidebar which will display the bar chart in the main frame.
def genre_bar():
    # Title in sidebar for bar chart
    bar_header = st.sidebar.subheader("Bar Chart of Top Genres:")
    # Button to display bar chart in main frame
    all_button = st.sidebar.button("Genres: All", key='bar')
    # Created an if statement if the user clicks the button
    if all_button:
        #Displays title in main frame for chart
        barchart_title = st.subheader("Bar Chart of Top Genres:")
        # Counts the number of times the general genre comes up
        spotify_df["Genre"].value_counts().plot(kind="barh")
        # Y-axis label
        plt.ylabel("Genre")
        # X-axis label
        plt.xlabel("Number of Songs in Data Set")
        # Gets rid of a warning that pops up, in order to make the dashboard easier to view for the user
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # Displays bar chart
        st.pyplot()
    return bar_header, all_button

# Creates a table of the top songs in each general genre, based on the overall genres that were created above. The table
# can be seen by clicking a button in the sidebar which will display the table in the main frame. The table will display
# specific information about the songs in that genre. The user can pick what genre in a drop down menu in the sidebar.
# We also renamed the columns in order to make the table easily understandable and easier to view for the user.
def top_songs():
    # Isolates the 'Genre' column from the dataframe
    genres = spotify_df["Genre"]
    # Creates an empty list of the genres
    genre_list = []
    # Creates a list of the genres so they do not repeat
    for i in genres:
        if i not in genre_list:
            genre_list.append(i)
    genres = genre_list
    # Title in sidebar for table
    table_header = st.sidebar.subheader("Top Genre Songs:")
    # Creates a selectbox for the user to choose what genre
    genre = st.sidebar.selectbox(label="Genres:", options=genres)
    # Button to display table in main frame
    songs_button = st.sidebar.button("Genre Top Songs", key='songs')
    # Isolates only certain columns we want shown in the table
    spotify_2 = spotify_df[['Title','Artist','Top Genre', 'Year', 'Danceability', 'Length (Duration)', 'Popularity', 'Grammy','Genre']]
    # Renames columns to be displayed on table
    spotify_2 = spotify_2.rename(columns={'Top Genre': 'Specific Genre', 'Length (Duration)': 'Length(in sec)'})
    # Created an if statement if the user clicks the button
    if songs_button:
        # Title in main frame
        st.subheader(f"Data on Top {genre} Songs:")
        # Sorts information to show the specific genre chosen and the top 5 songs in that genre based on popularity
        information = spotify_2.query(f"""Genre==@genre""").nlargest(5, "Popularity")
        # Displays table
        chart = st.table(information)
    return table_header, songs_button


# Creates a list of all of the possible years that show up in the dataframes  in order to not have repetitive years.
# Then, instead of having each year from 1956-2019 be an option, for the selectbox for the song filters in the main
# frame, we created decades in order to make it easier for the user to have many song options come up for in that time
# frame.

# Isolates 'Year' column from dataframe
years = spotify_df["Year"]
# Creates an empty list of years
year_list = []
# Creates a list of the years so they do not repeat
for i in years:
    if i not in year_list:
        year_list.append(i)
    years = year_list
# Creates an empty column for the decades
spotify_df['Decade'] = ""
# Iterate through each row in the data frame and put all of the years less than a specific year into an overall decade
for index, row in spotify_df.iterrows():
    if row['Year'] < 1960:
        row['Decade'] = '1950s'
    elif row['Year'] < 1970:
        row['Decade'] = '1960s'
    elif row['Year'] < 1980:
        row['Decade'] = '1970s'
    elif row['Year'] < 1990:
        row['Decade'] = '1980s'
    elif row['Year'] < 2000:
        row['Decade'] = '1990s'
    elif row['Year'] < 2010:
        row['Decade'] = '2000s'
    else:
        row['Decade'] = '2010s'
    # Sets year value for each particular row
    spotify_df["Decade"].loc[index] = row["Decade"]


# Creates a filtered table in the main frame that the user can adjust the results with the user of six sliders for song
# specifics such as duration, danceability, and more, along with a checkbox if the user wants the table to show songs
# that have received a grammy and also a selectbox to pick one or multiple decades. This creates an interactive table
# that the user can adjust the variables in order to have certain songs show.
def song_filter():
    # Creates a title in the mainframe
    st.subheader("Song filters with adjustable sliders:")
    global spotify_df
    # Isolates only certain columns we want shown in the table
    spotify_2 = spotify_df[['Title', 'Artist', 'Top Genre', 'Year', 'Energy','Danceability', 'Length (Duration)',
                            'Acousticness', 'Speechiness','Popularity', 'Grammy', 'Genre', 'Decade']]
    # Renames columns to be displayed on table
    spotify_2 = spotify_2.rename(columns={'Top Genre': 'Specific Genre', 'Length (Duration)': 'Length'})
    # Converts 'Popularity' column into a float data type
    spotify_2['Popularity'] = spotify_2['Popularity'].astype(float)
    # The following 6 variables create a slider for that variable with the min and max in a float data type
    danceability = st.slider('Danceability (drag slider to minimum amount)', float(spotify_2.Danceability.min()),
                             float(spotify_2.Danceability.max()), step=1., value = 50.)
    popularity = st.slider('Popularity (drag slider to minimum amount)', float(spotify_2.Popularity.min()),
                           float(spotify_2.Popularity.max()), step=1., value = 50.)
    energy = st.slider('Energy (drag slider to minimum amount)', float(spotify_2.Energy.min()),
                       float(spotify_2.Energy.max()), step=1., value = 50.)
    speechiness = st.slider('Speechiness (drag slider to minimum amount)', float(spotify_2.Speechiness.min()),
                            float(spotify_2.Speechiness.max()), step=1., value=25.)
    acousticness = st.slider('Acousticness (drag slider to maximum amount)', float(spotify_2.Acousticness.min()),
                             float(spotify_2.Acousticness.max()), step=1., value=50.)
    length = st.slider('Length in seconds (drag slider to maximum amount)', float(spotify_2.Length.min()),
                       float(spotify_2.Length.max()), step=1., value=500.)
    # Creates a checkbox for the user to decide if they want the songs in the table to have received a Grammy
    grammy = st.checkbox('Grammy', spotify_df['Grammy'].all())
    # Creates a selectbox where the user can choose multiple decades, from the decades we created above
    year = st.multiselect('Decade', spotify_df['Decade'].unique())
    # The following 8 lines of code distinguish how the variable will be treated in the table
    spotify_2 = spotify_2[spotify_2['Danceability'] > danceability]
    spotify_2 = spotify_2[spotify_2['Popularity'] > popularity]
    spotify_2 = spotify_2[spotify_2['Energy'] > energy]
    spotify_2 = spotify_2[spotify_2['Speechiness'] > speechiness]
    spotify_2 = spotify_2[spotify_2['Acousticness'] < acousticness]
    spotify_2 = spotify_2[spotify_2['Length'] < length]
    spotify_2 = spotify_2[spotify_2['Grammy'] == grammy]
    spotify_2 = spotify_2[spotify_2['Decade'].isin(year)]
    # Creates a table that is sorted and in an ascending order
    st.dataframe(spotify_2.sort_values(by=['Danceability', 'Popularity', 'Energy', 'Speechiness','Acousticness','Length','Grammy','Year'],
                                       ascending=False).reset_index(drop=True))


# Returns functions
image("spotifyimg.jpg", "")
genre_bar()
top_songs()
song_filter()




