import requests   #Implemented so the program can make HTTP requests
import pandas as pd                   #Data analysis package
import matplotlib.pyplot as plt      #Data Visualization package
import seaborn as sns                #Data Visualization package

Fourth_largest = {}
Offensive_Rebounds_per_game = []
Center_FP_per_game = []

#Function is getting data from an external source using a get request via an API
def getData():
	#using the API endpoint url the get method obtains data from the server
	URL = "https://api.sportsdata.io/v3/nba/stats/json/PlayerSeasonStats/2021"  #API endpoint
	#Dictionary to map HTTP authenticator and API key
	Headers = {"Ocp-Apim-Subscription-Key": "d22e84f5c1fa4f4ab47bf1419bd94221",  "accept": "application/json",}   
    #.json() method is used to used to return a JSON object
	response = requests.get(url = URL , headers = Headers).json()  #get request parameters to successfully request and receive data from API endpoint
	pd.DataFrame(response).to_csv("Fbballdata.csv", index=False) #Write oject to csv file

	FB = pd.read_csv('Fbballdata.csv')  
	FB.drop(['GlobalTeamID', 'IsClosed', 'LineupConfirmed', 'LineupStatus', 'Team', 'FantasyPoints', 'FantasyPointsDraftKings', 'FantasyPointsFanDuel', 
	'FantasyPointsFantasyDraft', 'FantasyPointsYahoo'], axis = 1, inplace = True)   #removing columns not necessary for data analysis
 
#dividing the data frame into five different data frames using filters, each data frame contains data for each position

	PG_filt = (FB['Position'] == 'PG') 
	PointGuard_FB = FB[PG_filt] #inner returns data series where the 'position' attribute is PG, data series is converted into dataframe
    
	SG_filt = (FB['Position'] == 'SG')
	ShootingGuard_FB = FB[SG_filt]

	SF_filt = (FB['Position'] == 'SF')
	SmallForward_FB = FB[SF_filt]
  
	PF_filt = (FB['Position'] == 'PF')
	PowerForward_FB = FB[PF_filt]

	Center_filt = (FB['Position'] == 'C')
	Center_FB = FB[Center_filt]
  
	#each function returns an updated dictionary
	#each function calculates the 3 players with the highest salaries
	dictionary = PG_Calc(PointGuard_FB)   
	dictionary = SG_Calc(ShootingGuard_FB, dictionary)
	dictionary = SF_Calc(SmallForward_FB, dictionary)
	dictionary = PF_Calc(PowerForward_FB, dictionary)
	dictionary = Center_Calc(Center_FB, dictionary)
	printResults(dictionary)   #prints out the results
	PlotChart(PointGuard_FB, ShootingGuard_FB, SmallForward_FB, PowerForward_FB, Center_FB)  #method used for data visualization
 
#This function uses a Panda's dataframe to calculate the fantasy points for each pointguard
def PG_Calc(PointGuard_FB):

	total_score = []
	three_pt_per_game = []
	turnovers = []
	assists = []
	Dict = {}
	Results_dict = {}
	
	for ind in PointGuard_FB.index:   #calculating fantasy points per game for each player (Traversing the dataframe row by row using index)
		total_points = 0
		if (int(PointGuard_FB['Assists'][ind]) != 0 and int(PointGuard_FB['Games'][ind] != 0)):
			assists_per_game = int(PointGuard_FB['Assists'][ind]) / int(PointGuard_FB['Games'][ind])
			total_points = total_points + 3 * assists_per_game
		else:
			assists_per_game = 0

		if (int(PointGuard_FB['Points'][ind] != 0) and int(PointGuard_FB['Games'][ind] != 0)):
			points_per_game = int(PointGuard_FB['Points'][ind]) / int(PointGuard_FB['Games'][ind])
			total_points = total_points + 3 * points_per_game	
		else:
			points_per_game = 0

		if (int(PointGuard_FB['OffensiveRebounds'][ind] != 0) and int(PointGuard_FB['Games'][ind] != 0)):
			OR_per_game = int(PointGuard_FB['OffensiveRebounds'][ind]) / int(PointGuard_FB['Games'][ind])
			total_points = total_points + 1.5 * OR_per_game
		else:
			OR_per_game = 0

		if (int(PointGuard_FB['DefensiveRebounds'][ind] != 0) and int(PointGuard_FB['Games'][ind] != 0)):
			DefensiveRebounds_per_game = int(PointGuard_FB['DefensiveRebounds'][ind]) / int(PointGuard_FB['Games'][ind])
			total_points = total_points + 1 * DefensiveRebounds_per_game
		else:
			DefensiveRebounds_per_game = 0

		if (int(PointGuard_FB['BlockedShots'][ind] != 0) and int(PointGuard_FB['Games'][ind] != 0)):
			BlockedShots_per_game = int(PointGuard_FB['BlockedShots'][ind]) / int(PointGuard_FB['Games'][ind])
			total_points = total_points + 2 * DefensiveRebounds_per_game
		else:
			BlockedShots_per_game = 0

		if (int(PointGuard_FB['Steals'][ind] != 0) and int(PointGuard_FB['Games'][ind] != 0)): 
			Steals_per_game = int(PointGuard_FB['Steals'][ind]) / int(PointGuard_FB['Games'][ind])
			total_points = total_points + 2 * Steals_per_game
		else:
			Steals_per_game = 0

		if (int(PointGuard_FB['FreeThrowsMade'][ind] != 0) and int(PointGuard_FB['Games'][ind] != 0)):  
			FreeThrowsMade_per_game = int(PointGuard_FB['Steals'][ind]) / int(PointGuard_FB['Games'][ind])
			total_points = total_points + 2.2 * FreeThrowsMade_per_game
		else:
			FreeThrowsMade_per_game = 0

		if (int(PointGuard_FB['TwoPointersMade'][ind] != 0) and int(PointGuard_FB['Games'][ind] != 0)): 
			TwoPointersMade_per_game = int(PointGuard_FB['TwoPointersMade'][ind]) / int(PointGuard_FB['Games'][ind])
		else:
			total_points = total_points + 2 * TwoPointersMade_per_game
			TwoPointersMade_per_game = 0

		if (int(PointGuard_FB['ThreePointersMade'][ind] != 0) and int(PointGuard_FB['Games'][ind] != 0)):  
			ThreePointersMade_per_game = int(PointGuard_FB['ThreePointersMade'][ind]) / int(PointGuard_FB['Games'][ind])
			total_points = total_points + 3 * ThreePointersMade_per_game
		else:
			ThreePointersMade_per_game = 0

		if (int(PointGuard_FB['Turnovers'][ind] != 0) and int(PointGuard_FB['Games'][ind] != 0)):  
			Turnovers_per_game = int(PointGuard_FB['Turnovers'][ind]) / int(PointGuard_FB['Games'][ind])
			total_points = total_points - 3 * Turnovers_per_game
			#PointGuard_FB['Turnovers_per_game'][ind] = Turnovers_per_game
		else:
			Turnovers_per_game = 0

		total_points = round(total_points, 1)
		
		#PointGuard_FB.insert(ind, 'FantasyPoints/GM', total_points)

		#Adding each stat to a list
		total_score.append(total_points)
		turnovers.append(Turnovers_per_game)
		assists.append(assists_per_game)
		three_pt_per_game.append(ThreePointersMade_per_game)
		Dict[PointGuard_FB['Name'][ind]] = total_points

	#converting list into a data series
	PointGuard_FB['FantasyPoints/GM'] = pd.Series(total_score)
	PointGuard_FB['Turnovers_per_game'] = turnovers
	PointGuard_FB['assists_per_game'] = assists
	PointGuard_FB['ThreePointersMade_per_game'] = three_pt_per_game

	print(PointGuard_FB['FantasyPoints/GM'])
		
	for key in Dict:
		print(key, ' : ' , Dict[key])

	max_key = max(Dict, key = Dict.get) #get() returns the key name of the item and the value mapped to the key
	print(max_key)
	max_value = Dict[max_key]
	print(max_value)

	Results_dict[max_key] = max_value #adding the draft picks to this list
	
	#Finding the player with the highest fantasy score using Dict's max function
	Max = max(Dict.values())
	second_max = 0
	third_max = 0
	fourth_max = 0
	
     #Findin the second highest, third highest, and fourth highest score
	for i in Dict.values():
 		if i > second_max and i < Max:
 			second_max = i
 		elif i > third_max and i < second_max:
 			third_max = i
 		elif i > fourth_max and i < third_max:
 		
 			fourth_max = i

 	#printing out the names and scores of the player found in the above dictionary
	for keys, values in Dict.items():
 		if values == second_max:
 			print(keys) 
 			print(values)
 			Results_dict[keys] = values
 		elif values == third_max:
 			print(keys) 
 			print(values)
 			Results_dict[keys] = values
 		elif values == fourth_max:
 			Fourth_largest[keys] = values
 			
	return Results_dict

#This function uses a Panda's dataframe to calculate the fantasy points for each shooting guard
def SG_Calc(ShootingGuard_FB, Results_dict):

	total_points = 0
	total_score = []
	three_points = []
	Dict = {}
	
	for ind in ShootingGuard_FB.index:   #calculating assists per game for each player (Traversing the dataframe row by row using index)
		total_points = 0
		if (int(ShootingGuard_FB['Assists'][ind]) != 0 and int(ShootingGuard_FB['Games'][ind] != 0)):
			assists_per_game = int(ShootingGuard_FB['Assists'][ind]) / int(ShootingGuard_FB['Games'][ind])
			total_points = total_points + 3 * assists_per_game
		else:
			assists_per_game = 0

		if (int(ShootingGuard_FB['Points'][ind] != 0) and int(ShootingGuard_FB['Games'][ind] != 0)):
			points_per_game = int(ShootingGuard_FB['Points'][ind]) / int(ShootingGuard_FB['Games'][ind])
			total_points = total_points + 3 * points_per_game
		else:
			points_per_game = 0

		if (int(ShootingGuard_FB['OffensiveRebounds'][ind] != 0) and int(ShootingGuard_FB['Games'][ind] != 0)):
			OR_per_game = int(ShootingGuard_FB['OffensiveRebounds'][ind]) / int(ShootingGuard_FB['Games'][ind])
			total_points = total_points + 1.5 * OR_per_game
		else:
			OR_per_game = 0

		if (int(ShootingGuard_FB['DefensiveRebounds'][ind] != 0) and int(ShootingGuard_FB['Games'][ind] != 0)):
			DefensiveRebounds_per_game = int(ShootingGuard_FB['DefensiveRebounds'][ind]) / int(ShootingGuard_FB['Games'][ind])
			total_points = total_points + 1 * DefensiveRebounds_per_game
		else:
			DefensiveRebounds_per_game = 0

		if (int(ShootingGuard_FB['BlockedShots'][ind] != 0) and int(ShootingGuard_FB['Games'][ind] != 0)):
			BlockedShots_per_game = int(ShootingGuard_FB['BlockedShots'][ind]) / int(ShootingGuard_FB['Games'][ind])
			total_points = total_points + 2 * DefensiveRebounds_per_game
		else:
			BlockedShots_per_game = 0

		if (int(ShootingGuard_FB['Steals'][ind] != 0) and int(ShootingGuard_FB['Games'][ind] != 0)): 
			Steals_per_game = int(ShootingGuard_FB['Steals'][ind]) / int(ShootingGuard_FB['Games'][ind])
			total_points = total_points + 2 * Steals_per_game
		else:
			Steals_per_game = 0

		if (int(ShootingGuard_FB['FreeThrowsMade'][ind] != 0) and int(ShootingGuard_FB['Games'][ind] != 0)):  
			FreeThrowsMade_per_game = int(ShootingGuard_FB['Steals'][ind]) / int(ShootingGuard_FB['Games'][ind])
			total_points = total_points + 2.2 * FreeThrowsMade_per_game
		else:
			FreeThrowsMade_per_game = 0

		if (int(ShootingGuard_FB['TwoPointersMade'][ind] != 0) and int(ShootingGuard_FB['Games'][ind] != 0)): 
			TwoPointersMade_per_game = int(ShootingGuard_FB['TwoPointersMade'][ind]) / int(ShootingGuard_FB['Games'][ind])
		else:
			total_points = total_points + 2 * TwoPointersMade_per_game
			TwoPointersMade_per_game = 0

		if (int(ShootingGuard_FB['ThreePointersMade'][ind] != 0) and int(ShootingGuard_FB['Games'][ind] != 0)):  
			ThreePointersMade_per_game = int(ShootingGuard_FB['ThreePointersMade'][ind]) / int(ShootingGuard_FB['Games'][ind])
			total_points = total_points + 3 * ThreePointersMade_per_game
		else:
			ThreePointersMade_per_game = 0

		if (int(ShootingGuard_FB['Turnovers'][ind] != 0) and int(ShootingGuard_FB['Games'][ind] != 0)):  
			Turnovers_per_game = int(ShootingGuard_FB['Turnovers'][ind]) / int(ShootingGuard_FB['Games'][ind])
			total_points = total_points - 3 * Turnovers_per_game
		else:
			Turnovers_per_game = 0

		total_points = round(total_points, 1) #rounding to the nearest tenth

		#list contains the stats
		three_points.append(ThreePointersMade_per_game)
		total_score.append(total_points)					
		Dict[ShootingGuard_FB['Name'][ind]] = total_points
		total_score.append(total_points)   #add this list as a value in a dictionary
		
	#converting the list to a series
	ShootingGuard_FB['FantasyPoints/GM'] = pd.Series(total_score)
	ShootingGuard_FB['ThreePointersMade/GM'] = pd.Series(three_points)
	print(ShootingGuard_FB['FantasyPoints/GM']) 
		
	print(ShootingGuard_FB)
	for key in Dict:
		print(key, ' : ' , Dict[key])

	max_key = max(Dict, key = Dict.get) #Finding the player with a highest fantasy score
	print(max_key)
	max_value = Dict[max_key]
	print(max_value)

	Results_dict[max_key] = max_value
	Max = max(Dict.values())
	second_max = 0
	third_max = 0
	fourth_max = 0

	#Finding second and third and fourth  highest fantasy score
	for i in Dict.values():
 		if i > second_max and i < Max:
 			second_max = i
 		elif i > third_max and i < second_max:
 			third_max = i
 		elif i > fourth_max and i < third_max:
 			fourth_max = i

    #Finding the associated values of the second, third, and fourth highest fantasy score
	for keys, values in Dict.items():
 		if values == second_max:
 			print(keys)
 			print(values)
 			Results_dict[keys] = values
 		elif values == third_max:
 			print(keys)
 			print(values)
 			Results_dict[keys] = values
 		elif values == fourth_max:
 			Fourth_largest[keys] = values

	return Results_dict

#This function uses a Panda's dataframe to calculate the fantasy points for each smallforward
def SF_Calc(SmallForward_FB, Results_dict):

	total_points = 0
	total_score = []
	Dict = {}
	
	for ind in SmallForward_FB.index:   #calculating fantasy points per game for each player (Traversing the dataframe row by row using index)
		total_points = 0
		if (int(SmallForward_FB['Assists'][ind]) != 0 and int(SmallForward_FB['Games'][ind] != 0)):
			assists_per_game = int(SmallForward_FB['Assists'][ind]) / int(SmallForward_FB['Games'][ind])
			total_points = total_points + 3 * assists_per_game
		else:
			assists_per_game = 0

		if (int(SmallForward_FB['Points'][ind] != 0) and int(SmallForward_FB['Games'][ind] != 0)):
			points_per_game = int(SmallForward_FB['Points'][ind]) / int(SmallForward_FB['Games'][ind])
			total_points = total_points + 3 * points_per_game
		else:
			points_per_game = 0

		if (int(SmallForward_FB['OffensiveRebounds'][ind] != 0) and int(SmallForward_FB['Games'][ind] != 0)):
			OR_per_game = int(SmallForward_FB['OffensiveRebounds'][ind]) / int(SmallForward_FB['Games'][ind])
			total_points = total_points + 1.5 * OR_per_game
		else:
			OR_per_game = 0

		if (int(SmallForward_FB['DefensiveRebounds'][ind] != 0) and int(SmallForward_FB['Games'][ind] != 0)):
			DefensiveRebounds_per_game = int(SmallForward_FB['DefensiveRebounds'][ind]) / int(SmallForward_FB['Games'][ind])
			total_points = total_points + 1 * DefensiveRebounds_per_game
		else:
			DefensiveRebounds_per_game = 0

		if (int(SmallForward_FB['BlockedShots'][ind] != 0) and int(SmallForward_FB['Games'][ind] != 0)):
			BlockedShots_per_game = int(SmallForward_FB['BlockedShots'][ind]) / int(SmallForward_FB['Games'][ind])
			total_points = total_points + 2 * DefensiveRebounds_per_game
		else:
			BlockedShots_per_game = 0

		if (int(SmallForward_FB['Steals'][ind] != 0) and int(SmallForward_FB['Games'][ind] != 0)): 
			Steals_per_game = int(SmallForward_FB['Steals'][ind]) / int(SmallForward_FB['Games'][ind])
			total_points = total_points + 2 * Steals_per_game
		else:
			Steals_per_game = 0

		if (int(SmallForward_FB['FreeThrowsMade'][ind] != 0) and int(SmallForward_FB['Games'][ind] != 0)):  
			FreeThrowsMade_per_game = int(SmallForward_FB['Steals'][ind]) / int(SmallForward_FB['Games'][ind])
			total_points = total_points + 2.2 * FreeThrowsMade_per_game
		else:
			FreeThrowsMade_per_game = 0

		if (int(SmallForward_FB['TwoPointersMade'][ind] != 0) and int(SmallForward_FB['Games'][ind] != 0)): 
			TwoPointersMade_per_game = int(SmallForward_FB['TwoPointersMade'][ind]) / int(SmallForward_FB['Games'][ind])
		else:
			total_points = total_points + 2 * TwoPointersMade_per_game
			TwoPointersMade_per_game = 0

		if (int(SmallForward_FB['ThreePointersMade'][ind] != 0) and int(SmallForward_FB['Games'][ind] != 0)):  
			ThreePointersMade_per_game = int(SmallForward_FB['ThreePointersMade'][ind]) / int(SmallForward_FB['Games'][ind])
			total_points = total_points + 3 * ThreePointersMade_per_game
		else:
			ThreePointersMade_per_game = 0

		if (int(SmallForward_FB['Turnovers'][ind] != 0) and int(SmallForward_FB['Games'][ind] != 0)):  
			Turnovers_per_game = int(SmallForward_FB['Turnovers'][ind]) / int(SmallForward_FB['Games'][ind])
			total_points = total_points - 3 * Turnovers_per_game
		else:
			Turnovers_per_game = 0

		total_points = round(total_points, 1)
		total_score.append(total_points)
		Dict[SmallForward_FB['Name'][ind]] = total_points								
	  #add this list as a value in a dictionary
	
	SmallForward_FB['FantasyPoints/GM'] = pd.Series(total_score)   #add the total_points for each player to the framework by adding a new column FantasyPoints/GM
	print(SmallForward_FB)
	
	for key in Dict:
		print(key, ' : ' , Dict[key])

	max_key = max(Dict, key = Dict.get)
	print(max_key)
	max_values = Dict[max_key]
	print(max_values)

	Results_dict[max_key] = max_values
	Max = max(Dict.values())
	second_max = 0
	third_max = 0
	fourth_max = 0

	#Finding second and third and fourth  highest fantasy score
	for i in Dict.values():
 		if i > second_max and i < Max:
 			second_max = i
 		elif i > third_max and i < second_max:
 			third_max = i
 		elif i > fourth_max and i < third_max:
 			fourth_max = i

 	#Finding the associated values of the second, third, and fourth highest fantasy score
	for keys, values in Dict.items():
 		if values == second_max:
 			print(keys)
 			print(values)
 			Results_dict[keys] = values
 		elif values == third_max:
 			print(keys)
 			print(values)
 			Results_dict[keys] = values
 		elif values == fourth_max:
 			Fourth_largest[keys] = values

	return Results_dict

#This function uses a Panda's dataframe to calculate the fantasy points for each Power Forward
def PF_Calc(PowerForward_FB,  Results_dict):

	total_points = 0
	total_score = []
	Dict = {}

	for ind in PowerForward_FB.index:   #calculating fantasy points per game for each player (Traversing the dataframe row by row using index)
		total_points = 0
		if (int(PowerForward_FB['Assists'][ind]) != 0 and int(PowerForward_FB['Games'][ind] != 0)):
			assists_per_game = int(PowerForward_FB['Assists'][ind]) / int(PowerForward_FB['Games'][ind])
			total_points = total_points + 3 * assists_per_game
		else:
			assists_per_game = 0

		if (int(PowerForward_FB['Points'][ind] != 0) and int(PowerForward_FB['Games'][ind] != 0)):
			points_per_game = int(PowerForward_FB['Points'][ind]) / int(PowerForward_FB['Games'][ind])
			total_points = total_points + 3 * points_per_game
		else:
			points_per_game = 0

		if (int(PowerForward_FB['OffensiveRebounds'][ind] != 0) and int(PowerForward_FB['Games'][ind] != 0)):
			OR_per_game = int(PowerForward_FB['OffensiveRebounds'][ind]) / int(PowerForward_FB['Games'][ind])
			total_points = total_points + 1.5 * OR_per_game
		else:
			OR_per_game = 0

		if (int(PowerForward_FB['DefensiveRebounds'][ind] != 0) and int(PowerForward_FB['Games'][ind] != 0)):
			DefensiveRebounds_per_game = int(PowerForward_FB['DefensiveRebounds'][ind]) / int(PowerForward_FB['Games'][ind])
			total_points = total_points + 1 * DefensiveRebounds_per_game
		else:
			DefensiveRebounds_per_game = 0

		if (int(PowerForward_FB['BlockedShots'][ind] != 0) and int(PowerForward_FB['Games'][ind] != 0)):
			BlockedShots_per_game = int(PowerForward_FB['BlockedShots'][ind]) / int(PowerForward_FB['Games'][ind])
			total_points = total_points + 2 * DefensiveRebounds_per_game
		else:
			BlockedShots_per_game = 0

		if (int(PowerForward_FB['Steals'][ind] != 0) and int(PowerForward_FB['Games'][ind] != 0)): 
			Steals_per_game = int(PowerForward_FB['Steals'][ind]) / int(PowerForward_FB['Games'][ind])
			total_points = total_points + 2 * Steals_per_game
		else:
			Steals_per_game = 0

		if (int(PowerForward_FB['FreeThrowsMade'][ind] != 0) and int(PowerForward_FB['Games'][ind] != 0)):  
			FreeThrowsMade_per_game = int(PowerForward_FB['Steals'][ind]) / int(PowerForward_FB['Games'][ind])
			total_points = total_points + 2.2 * FreeThrowsMade_per_game
		else:
			FreeThrowsMade_per_game = 0

		if (int(PowerForward_FB['TwoPointersMade'][ind] != 0) and int(PowerForward_FB['Games'][ind] != 0)): 
			TwoPointersMade_per_game = int(PowerForward_FB['TwoPointersMade'][ind]) / int(PowerForward_FB['Games'][ind])
		else:
			total_points = total_points + 2 * TwoPointersMade_per_game
			TwoPointersMade_per_game = 0

		if (int(PowerForward_FB['ThreePointersMade'][ind] != 0) and int(PowerForward_FB['Games'][ind] != 0)):  
			ThreePointersMade_per_game = int(PowerForward_FB['ThreePointersMade'][ind]) / int(PowerForward_FB['Games'][ind])
			total_points = total_points + 3 * ThreePointersMade_per_game
		else:
			ThreePointersMade_per_game = 0

		if (int(PowerForward_FB['Turnovers'][ind] != 0) and int(PowerForward_FB['Games'][ind] != 0)):  
			Turnovers_per_game = int(PowerForward_FB['Turnovers'][ind]) / int(PowerForward_FB['Games'][ind])
			total_points = total_points - 3 * Turnovers_per_game
		else:
			Turnovers_per_game = 0
		
		total_points = round(total_points, 1)
		total_score.append(total_points)   #add this list as a value in a dictionary
		Dict[PowerForward_FB['Name'][ind]] = total_points
		
	PowerForward_FB['FantasyPoints/GM'] = pd.Series(total_score)
	print(PowerForward_FB)
	for key in Dict:
		print(key, ' : ' , Dict[key])

	max_key = max(Dict, key = Dict.get) #Finding the highest number of fantasy points in dictionary
	print(max_key)
	max_value = Dict[max_key] #FInding player associated with the highest number of fantasy points in the given dictionary
	print(max_value)

	Results_dict[max_key] = max_value
	Max = max(Dict.values())
	second_max = 0
	third_max = 0
	fourth_max = 0

	#Finding second and third and fourth  highest fantasy score
	for i in Dict.values():
 		if i > second_max and i < Max:
 			second_max = i
 		elif i > third_max and i < second_max:
 			third_max = i
 		elif i > fourth_max and i < third_max:
 			fourth_max = i

 	#Finding the associated values of the second, third, and fourth highest fantasy score
	for keys, values in Dict.items():
 		if values == second_max:
 			print(keys)
 			print(values)
 			Results_dict[keys] = values
 		elif values == third_max:
 			Results_dict[keys] = values
 		elif values == fourth_max:
 			Fourth_largest[keys] = values

	return Results_dict

#This function uses a Panda's dataframe to calculate the fantasy points for each Center. 
def Center_Calc(Center_FB,  Results_dict):

	total_points = 0
	total_score = []
	rebounds = []
	blocks = []
	Dict = {}

	ORG = pd.DataFrame()
	
	for ind in Center_FB.index:   #calculating assists per game for each player (Traversing the dataframe row by row using index)
		total_points = 0
		if (int(Center_FB['Assists'][ind]) != 0 and int(Center_FB['Games'][ind] != 0)):
			assists_per_game = int(Center_FB['Assists'][ind]) / int(Center_FB['Games'][ind])
			total_points = total_points + 3 * assists_per_game
		else:
			assists_per_game = 0

		if (int(Center_FB['Points'][ind] != 0) and int(Center_FB['Games'][ind] != 0)):
			points_per_game = int(Center_FB['Points'][ind]) / int(Center_FB['Games'][ind])
			total_points = total_points + 3 * points_per_game
		else:
			points_per_game = 0

		if (int(Center_FB['OffensiveRebounds'][ind] != 0) and int(Center_FB['Games'][ind] != 0)):
			OR_per_game = int(Center_FB['OffensiveRebounds'][ind]) / int(Center_FB['Games'][ind])
			total_points = total_points + 1.5 * OR_per_game
		else:
			OR_per_game = 0

		if (int(Center_FB['DefensiveRebounds'][ind] != 0) and int(Center_FB['Games'][ind] != 0)):
			DefensiveRebounds_per_game = int(Center_FB['DefensiveRebounds'][ind]) / int(Center_FB['Games'][ind])
			total_points = total_points + 1 * DefensiveRebounds_per_game
		else:
			DefensiveRebounds_per_game = 0

		if (int(Center_FB['BlockedShots'][ind] != 0) and int(Center_FB['Games'][ind] != 0)):
			BlockedShots_per_game = int(Center_FB['BlockedShots'][ind]) / int(Center_FB['Games'][ind])
			total_points = total_points + 2 * DefensiveRebounds_per_game
		else:
			BlockedShots_per_game = 0

		if (int(Center_FB['Steals'][ind] != 0) and int(Center_FB['Games'][ind] != 0)): 
			Steals_per_game = int(Center_FB['Steals'][ind]) / int(Center_FB['Games'][ind])
			total_points = total_points + 2 * Steals_per_game
		else:
			Steals_per_game = 0

		if (int(Center_FB['FreeThrowsMade'][ind] != 0) and int(Center_FB['Games'][ind] != 0)):  
			FreeThrowsMade_per_game = int(Center_FB['Steals'][ind]) / int(Center_FB['Games'][ind])
			total_points = total_points + 2.2 * FreeThrowsMade_per_game
		else:
			FreeThrowsMade_per_game = 0

		if (int(Center_FB['TwoPointersMade'][ind] != 0) and int(Center_FB['Games'][ind] != 0)): 
			TwoPointersMade_per_game = int(Center_FB['TwoPointersMade'][ind]) / int(Center_FB['Games'][ind])
			total_points = total_points + 2 * TwoPointersMade_per_game
		else:
			TwoPointersMade_per_game = 0

		if (int(Center_FB['ThreePointersMade'][ind] != 0) and int(Center_FB['Games'][ind] != 0)):  
			ThreePointersMade_per_game = int(Center_FB['ThreePointersMade'][ind]) / int(Center_FB['Games'][ind])
			total_points = total_points + 3 * ThreePointersMade_per_game
		else:
			ThreePointersMade_per_game = 0

		if (int(Center_FB['Turnovers'][ind] != 0) and int(Center_FB['Games'][ind] != 0)):  
			Turnovers_per_game = int(Center_FB['Turnovers'][ind]) / int(Center_FB['Games'][ind])
			total_points = total_points - 3 * Turnovers_per_game
		else:
			Turnovers_per_game = 0
		
		
		total_rebounds_pergame = DefensiveRebounds_per_game + OR_per_game
		total_points = round(total_points, 1)
		Dict[Center_FB['Name'][ind]] = total_points
		
		#add the stats calculated to a list
		total_score.append(total_points)   
		blocks.append(BlockedShots_per_game)
		rebounds.append(total_rebounds_pergame)
		Offensive_Rebounds_per_game.append(OR_per_game)
		Center_FP_per_game.append(total_points)

	#Converting the list into a dataframe
	Center_FB['FantasyPoints/GM'] = total_score
	Center_FB['Blocks_per_Game'] = blocks
	Center_FB['Rebounds_per_game'] = rebounds
	Center_FB['Offensive_Rebounds_per_game'] = Offensive_Rebounds_per_game

	#print players and their fantasy points
	for key in Dict:
		print(key, ' : ' , Dict[key])

	#Finding the player with the highest number of points
	max_key = max(Dict, key = Dict.get)
	print(max_key)
	max_values = Dict[max_key]   #Finding the number of points the top player scored
	print(max_values)
	Results_dict[max_key] = max_values #adding to results_dict dictionary whcih 
	
	Max = max(Dict.values())  
	second_max = 0
	third_max = 0
	fourth_max = 0

	#Finding second and third and fourth  highest fantasy score
	for i in Dict.values():
 		if i > second_max and i < Max:
 			second_max = i
 		elif i > third_max and i < second_max:
 			third_max = i
 		elif i > fourth_max and i < third_max:
 			fourth_max = i

 	#Finding the associated values of the second, third, and fourth highest fantasy score
	for keys, values in Dict.items():
 		if values == second_max:
 			print(keys)
 			print(values)
 			Results_dict[keys] = values
 		elif values == third_max:
 			print(keys)
 			print(values)
 			Results_dict[keys] = values
 		elif values == fourth_max:
 			Fourth_largest[keys] = values
 			
	return Results_dict

#This function prints out the players who should be drafted and the predicted fantasy score
def printResults(dictionary):
	print("\n\nFinal Output(Suggested draft and Plots):")
	print("\n\n\nDraft Picks and Projected Scores: ")

	#printing out players/fantasy points in dictionary which contains top3 players from each position plus an extra player
	for keys, values in dictionary.items():
		print(keys, ":", values)
	
	max_key = max(Fourth_largest, key = Fourth_largest.get) #used to select the 13th player (take 4th highest player from all positions and take the highest of all 4)
	max_val = Fourth_largest[max_key]
	print(max_key, ':',  max_val)



 #This method is using matplotlib and seaborn for data visualization
 #Visualizing data to show the correlation between the statistics and the fantasy points per game for specific positions
def PlotChart(PointGuard_FB, ShootingGuard_FB, SmallForward_FB, PowerForward_FB, Center_FB):

	fig_dims = (8, 7)  #setting the size of the figure created
	fig, axs = plt.subplots(nrows = 3, ncols=3, figsize = fig_dims)  #creating nine subplots in the figure
	sns.set_style('whitegrid')

	#Each statistic is assigned a series, the series method is used to give the columns names which will be used for the x/y-axis 
	#merge function is used to combine the series into a new dataframe which will be passed as the data param in the regplot
	#function

	#Nine plots depicting the following correlations

	#1) Offensive Rebound per game vs Center Fantasy Points per game
	OR_per_game_series = pd.Series(Center_FB['Offensive_Rebounds_per_game'], name = "Center_OffensiveRebounds_Per_Game")
	Center_FP_per_game_series = pd.Series(Center_FB['FantasyPoints/GM'], name = "Center_FP_Per_Game")
	dat = pd.merge(OR_per_game_series, Center_FP_per_game_series, right_index = True, left_index = True)

	#2) #rebounds per game vs center fantasy points per game
	Center_Rebounds_Series = pd.Series(Center_FB['Rebounds_per_game'], name = "Center_Rebounds_per_Game")
	Center_Data = pd.merge(Center_Rebounds_Series, Center_FP_per_game_series, right_index = True, left_index = True)
	
	#3) assists per game vs point guard assists per game
	PG_assists_series = pd.Series(PointGuard_FB['assists_per_game'], name = "PG_Assists_Per_Game")
	PG_Fantasy_Points_series = pd.Series(PointGuard_FB['FantasyPoints/GM'], name = "PG_FP_Per_Game")
	PG_data = pd.merge(PG_assists_series, PG_Fantasy_Points_series, right_index = True, left_index = True)

	#4) Blocks per game vs center fantasy points per game
	Blocks_per_game_series = pd.Series(Center_FB['Blocks_per_Game'], name = 'Blocks_Per_Game')
	Center_BlocksCorrelation_Data = pd.merge(Blocks_per_game_series, Center_FP_per_game_series, right_index = True, left_index = True)

	#5) Turnovers per game vs PG fantasy points per game
	Turnovers_per_game_series = pd.Series(PointGuard_FB['Turnovers_per_game'], name = 'Turnovers_Per_Game')
	PG_TurnoversCorrelation_Data = pd.merge(Turnovers_per_game_series, PG_Fantasy_Points_series, right_index = True, left_index = True)

	#6) ThreePointsMadeper game vs PG fantasy points per game
	ThreePointsMade_per_game_series = pd.Series(PointGuard_FB['ThreePointersMade_per_game'], name = '3PtsMade_Per_Game')
	PG_ThreePoint_Corr_data = pd.merge(ThreePointsMade_per_game_series, PG_Fantasy_Points_series, right_index = True, left_index = True) 
	
	#7) ThreePointsMadeperGame vs SG fantasy points per game
	SG_3ptsper_series = pd.Series(ShootingGuard_FB['ThreePointersMade/GM'], name = '3PTSMade_Per_Game')
	SG_FantasyPoints_Series = pd.Series(ShootingGuard_FB['FantasyPoints/GM'], name = 'SG_FP_Per_Game')
	SG_ThreePoint_Corr_Data = pd.merge(SG_3ptsper_series, SG_FantasyPoints_Series, right_index = True, left_index = True)

	#8) Rebounds per game vs PF fantasy points per game
	PF_FantasyPoints_series = pd.Series(PowerForward_FB['FantasyPoints/GM'], name = 'PF_FP_Per_Game')
	PF_Rebounds_pergame_series = pd.Series(PowerForward_FB['OffensiveRebounds'], name = 'PF_OffensiveRebounds_PerGame')
	PF_Corr_Data = pd.merge(PF_FantasyPoints_series, PF_Rebounds_pergame_series, right_index = True, left_index = True )

	#9) FreeThrowsMade per game vs SF Fantasy Points per game
	SF_FantasyPoints_Series = pd.Series(SmallForward_FB['FantasyPoints/GM'], name = 'SF_FP_Per_Game') 
	SF_FreeThrowsMade_Series = pd.Series(SmallForward_FB['FreeThrowsMade'], name = 'SF_FreeThrowsMade_Per_Game')
	SF_Corr_Data = pd.merge(SF_FantasyPoints_Series, SF_FreeThrowsMade_Series, right_index = True, left_index = True)

	#Create a scatter plot with a regression line
	#paramaters: xlabels, ylabels, data param (dataframe which contains the data used for x/y variables, ax param determines whcih subplot will be allocated for this plot
	#, line_kws params determines the color of the regression line, and scatter_kws param determines the color of the dots)
	sns.regplot(x = 'Center_OffensiveRebounds_Per_Game', y = 'Center_FP_Per_Game', data = dat, ax = axs[0][0], line_kws={"color": "red"}, scatter_kws={"color": "black"})
	sns.regplot(x = 'Center_Rebounds_per_Game', y = 'Center_FP_Per_Game', data = Center_Data, ax= axs[0][1], line_kws={"color": "red"}, scatter_kws={"color": "black"})
	sns.regplot(x = 'PG_Assists_Per_Game', y = 'PG_FP_Per_Game', data = PG_data, ax = axs[0][2], line_kws={"color": "red"}, scatter_kws={"color": "black"})
	sns.regplot(x = 'Blocks_Per_Game' , y = 'Center_FP_Per_Game' , data = Center_BlocksCorrelation_Data , ax = axs[1][0], line_kws={"color": "red"}, scatter_kws={"color": "black"})
	sns.regplot(x = 'Turnovers_Per_Game', y = 'PG_FP_Per_Game', data = PG_TurnoversCorrelation_Data, ax = axs[1][1], line_kws={"color": "red"}, scatter_kws={"color": "black"})
	sns.regplot(x = '3PtsMade_Per_Game', y = 'PG_FP_Per_Game', data = PG_ThreePoint_Corr_data, ax = axs[1][2], line_kws={"color": "red"}, scatter_kws={"color": "black"})
	sns.regplot(x = '3PTSMade_Per_Game', y = 'SG_FP_Per_Game', data = SG_ThreePoint_Corr_Data, ax = axs[2][0], line_kws={"color": "red"}, scatter_kws={"color": "black"})
	sns.regplot(x = 'PF_OffensiveRebounds_PerGame', y ='PF_FP_Per_Game', data = PF_Corr_Data, ax = axs[2][1], line_kws={"color": "red"}, scatter_kws={"color": "black"})
	sns.regplot(x = 'SF_FreeThrowsMade_Per_Game', y = 'SF_FP_Per_Game', data = SF_Corr_Data, ax = axs[2][2], line_kws={"color": "red"}, scatter_kws={"color": "black"})
	fig.tight_layout(rect=[0, 0.03, 1, 0.85], pad = 2) #tight_layout spaces out the subplots
	fig.suptitle("Fantasy Basketball Statistical Analysis (Correlation between stats and fantasy points)", fontsize = 16) #Title of the figure and its size
	plt.legend(labels=['Regression_Line', 'Scatter_Points'], bbox_to_anchor=(1.01, 1), borderaxespad=0, loc = 'upper center')
	

	plt.show()   #depict the figure and its subplots as output


	return

#Call get data functiojn
getData()


