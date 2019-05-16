#This is a function library for mod2 project

import sqlite3 as sqlite3
import pandas as pd
import matplotlib.pyplot as plt
# from pathlib import Path

# def con_sql(db_name, dialect=None):
# 	db_file = Path(db_name)
# 	if not db_file.is_file():
# 		print("no such database file: {}".format(db_name))
# 		return
# 	if dialect is None:
# 		return sqlite3.connect(db_name)
# 	return sqlite3.connect(db_name, dialect)


conn = sqlite3.Connection('database.sqlite')
c = conn.cursor()

c.execute('''SELECT Season
            FROM Matches
            WHERE Season=2011''').fetchall()

class Team:
    def __init__(self, name):
        self.name = name
        self.record = None
        self.goals_scored = None
        self.game_dates_and_results_list = None

    #Gets a list of tuples of all the dates a team played 
    # and a binary value for whether they won or lost in the format (date, 1) or (date, 0)
    def set_game_dates_and_results_list(self):
        q=("""
        SELECT Date, FTR, HomeTeam, AwayTeam, Season
        FROM Matches 
        WHERE (Season=2011) AND ((HomeTeam='{}') OR (AwayTeam='{}'))
        ORDER BY Date
        """.format(self.name, self.name))

        df = pd.read_sql_query(q, conn)
        date_result_tuple_list = []
        for i, date in enumerate(df.Date):
            if df.FTR[i]=='H' and df.HomeTeam[i]==self.name:
                date_result_tuple_list.append((df.Date[i], 'W'))
            elif df.FTR[i]=='H' and df.HomeTeam[i]!=self.name:
                date_result_tuple_list.append((df.Date[i], 'L'))
            elif df.FTR[i]=='A' and df.AwayTeam[i]==self.name:
                date_result_tuple_list.append((df.Date[i], 'W'))
            elif df.FTR[i]=='A' and df.AwayTeam[i]!=self.name:
                date_result_tuple_list.append((df.Date[i], 'L'))
            else:
                date_result_tuple_list.append((df.Date[i], 'D'))

        self.game_dates_and_results_list = date_result_tuple_list

    #Sets the Team's GOALS SCORED
    def set_goals_scored(self):
        q=("""
        SELECT FTHG, FTAG
        FROM Matches
        WHERE (Season=2011) AND ((HomeTeam='{}') OR (AwayTeam='{}'))
        """.format(self.name, self.name))

        df = pd.read_sql_query(q, conn)
        total_goals = df.FTHG.sum() + df.FTAG.sum()
        self.goals_scored = total_goals

    #Sets the Team's RECORD
    def set_record(self):
        #This finds the wins
        q=("""
        SELECT FTR, HomeTeam, AwayTeam, Season  
        FROM Matches
        WHERE ((Season=2011) AND (HomeTeam='{}')) AND (FTR='H') OR ((Season=2011) AND (AwayTeam='{}')) AND (FTR='A')
        """.format(self.name,self.name))

        wins = pd.read_sql_query(q, conn)
        num_wins = wins.shape[0]

        #This finds the losses
        q=("""
        SELECT FTHG, FTAG, FTR, HomeTeam, AwayTeam, Season  
        FROM Matches
        WHERE ((Season=2011) AND (HomeTeam='{}')) AND (FTR='A') OR ((Season=2011) AND (AwayTeam='{}')) AND (FTR='H')
        """.format(self.name,self.name))

        losses = pd.read_sql_query(q, conn)
        num_losses = losses.shape[0]

        #This finds the drawws
        q=("""
        SELECT FTHG, FTAG, FTR, HomeTeam, AwayTeam, Season  
        FROM Matches
        WHERE ((Season=2011) AND (HomeTeam='{}')) AND (FTR='D') OR ((Season=2011) AND (AwayTeam='{}')) AND (FTR='D')
        """.format(self.name,self.name))

        draws = pd.read_sql_query(q, conn)
        num_draws = draws.shape[0]
        print(num_wins)
        self.record = [num_wins,num_losses,num_draws]


BM = Team('Bayern Munich')
BM.set_record
print(f'the record of Bayern Munich is: {BM.record}')



#Gets a list of all the teams that played in the 2011 season
def get_team_list():
        q=("""
        SELECT TeamName  
        FROM Unique_Teams u
        JOIN Matches m
        WHERE (u.TeamName=m.HomeTeam) OR (u.TeamName=m.AwayTeam) AND (m.Season=2011)
        """)
        df = pd.read_sql_query(q, conn)
        df.drop_duplicates('TeamName', inplace=True)
        team_name_list = list(df.TeamName)
        
        return team_name_list

