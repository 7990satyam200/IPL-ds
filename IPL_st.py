import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns
from PIL import Image
Ipl_image= Image.open("Iplll.jpg")
srh= Image.open("team_images/srh.jpg")
kkr= Image.open("team_images/kkr.jpg")


matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')


st.title("IPL data analyis over 2009 to 2020")

choice = st.sidebar.radio("Teamwise analyis or Overall Analysis.", ('Overall', 'Team'))
if choice == 'Team':
	option = st.selectbox("Which is your favourite team?", matches.winner.unique().tolist())
	if st.button("Go"):
		st.write("Oh! You like {}. Great!".format(option))
		if option=="Sunrisers Hyderabad":
			st.image(srh, use_column_width= True)
		elif option=="Kolkata Knight Riders":
			st.image(kkr, use_column_width= True)
		else:
			st.image(kkr, use_column_width= True)
else:
	st.image(Ipl_image, use_column_width= True)






match_data_enable = st.sidebar.checkbox("Show Data About All Matches Data")

if match_data_enable:
	st.write("Data about Matches.")
	st.dataframe(matches.head())

deliveries_data_enable = st.sidebar.checkbox("Show Data About All deliveries")

if deliveries_data_enable:
	st.write("Data about deliveries.")
	st.dataframe(deliveries.head())




defautcols = ["city", "player_of_match", "winner","team1", "team2"]
cols = st.sidebar.multiselect("Columns", matches.columns.tolist(), default = defautcols)



season_filter = st.sidebar.checkbox("Filter Based on Season")

if season_filter:
	cols = st.sidebar.multiselect("Select Year", matches.season.unique().tolist(), default=2019)
	a= matches.season.isin(cols)
	Winning_Filter = st.sidebar.checkbox("Filter Based on Winning Team")

	if Winning_Filter:
		cols = st.sidebar.multiselect("Select Winner", matches.winner.unique().tolist(), default='Mumbai Indians')
		b = matches.winner.isin(cols)
		st.dataframe(matches[(a & b)])
	else:
		st.dataframe(matches[a])



player_of_match_filter = st.sidebar.checkbox("Filter Based on Player of Match")



city_filter = st.sidebar.checkbox("Filter Based on City")

if city_filter:
		cols = st.sidebar.multiselect("Select City", matches.city.unique().tolist(), default='Mumbai')
		b = matches.city.isin(cols)
		st.dataframe(matches[(a & b)])


if player_of_match_filter:
	cols = st.sidebar.multiselect("Select Player of Match", matches.player_of_match.unique().tolist(), default='Yuvraj Singh')
	st.dataframe(matches[matches.player_of_match.isin(cols)])




team_info = st.sidebar.checkbox("Display Teamwise Summary of Data.")
team_plot = st.sidebar.checkbox("Display Teamwise Plotß")



myaggr= {'win_by_runs':'max', 'win_by_wickets':'max', 'city':'count'}
By_winning = matches.groupby(['winner'])
By_winning= By_winning['win_by_runs', 'win_by_wickets', 'city'].agg(myaggr)
By_winning.columns = ['All_Winnings', 'Highest_win_by_wickets', 'Highest_win_by_runs']
By_winning = By_winning.sort_values(by= ['All_Winnings'], ascending= False)
By_winning= By_winning.reset_index()
By_winning['relative'] = By_winning.All_Winnings/np.sum(By_winning.All_Winnings.values)
if team_info:
   st.dataframe(By_winning)

if team_plot:
	genre = st.sidebar.radio("What's your favorite movie genre",('Winner vs Total Winnings', 'Winner vs win by runs'))
	if genre == 'Winner vs Total Winnings':
	 sns.catplot(x="All_Winnings", y= "winner", data = By_winning, kind= "bar")
	 st.pyplot()
	else:
		sns.catplot(x="Highest_win_by_runs", y= "winner", data = By_winning, kind= "bar")
		st.pyplot()





TeamsALLtimeperformance = pd.read_csv('TeamsALLtimeperformance.csv', index_col='season')

defautcols = ['Kolkata Knight Riders', 'Mumbai Indians']
cols = st.sidebar.multiselect("Columns", TeamsALLtimeperformance.columns.tolist(), default = defautcols)
selectedTeamsPerforma = TeamsALLtimeperformance[cols]
st.line_chart(selectedTeamsPerforma)
