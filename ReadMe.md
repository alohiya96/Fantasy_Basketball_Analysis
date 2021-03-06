ReadMe.md

Fantasy Basketball Statistics Analysis and Draft Selection:

This repo contains the code which can be used by fantasy basketball users to choose which players to draft using realtime data. 

The program uses an API to extract the code from the website, store the code in a Pandas dataframe, and use the different functions in the Panda's library to
create new data frames and select specific columns of data to calculate the fantasy points of each player. Then, the program uses a dictionary to map the player's name, and the number of points he has scored.

The code performs a data analysis and outputs the 14 players, the player should draft.

The matplotlib and seaborn library is used for data visualization to depict the correlations between the statisitics and a player's performance by position. There are 6 regression plots in this project which show the correlations between the following stats: 

1) Offensive Rebounds per Game -> Center Fantasy Points per Game
2) Point Guard Assists per Game -> Point Guard Fantasy Points per Game
3) Blocks per Game -> Center Fantasy Points per Game
4) Turnovers per Game -> Point Guard Fantasy Points per Game
5) Three Points Made per Game -> Point Guard Fantasy Points per Game
6) Three Points per Game -> Shooting Guard Fantasy Points per Game
7) Three Points Made per Game -> Shooting Guard Fantasy Points per Game
8) Offensive Rebounds Per Game -> Power Forward Fantasy Points per Game
9) Small Forward Free Throws Made per Game -> Small Forward Fantasy Points per Game 

Installation:

1) User should install python3 
2) Create a virtual environment
3) Install the required packages with pip install -r requirements.txt




