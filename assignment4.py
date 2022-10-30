#!/usr/bin/env python
# coding: utf-8

# # Assignment 4
# ## Description
# In this assignment you must read in a file of metropolitan regions and associated sports teams from [assets/wikipedia_data.html](assets/wikipedia_data.html) and answer some questions about each metropolitan region. Each of these regions may have one or more teams from the "Big 4": NFL (football, in [assets/nfl.csv](assets/nfl.csv)), MLB (baseball, in [assets/mlb.csv](assets/mlb.csv)), NBA (basketball, in [assets/nba.csv](assets/nba.csv) or NHL (hockey, in [assets/nhl.csv](assets/nhl.csv)). Please keep in mind that all questions are from the perspective of the metropolitan region, and that this file is the "source of authority" for the location of a given sports team. Thus teams which are commonly known by a different area (e.g. "Oakland Raiders") need to be mapped into the metropolitan region given (e.g. San Francisco Bay Area). This will require some human data understanding outside of the data you've been given (e.g. you will have to hand-code some names, and might need to google to find out where teams are)!
# 
# For each sport I would like you to answer the question: **what is the win/loss ratio's correlation with the population of the city it is in?** Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. Remember that to calculate the correlation with [`pearsonr`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html), so you are going to send in two ordered lists of values, the populations from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. Average the win/loss ratios for those cities which have multiple teams of a single sport. Each sport is worth an equal amount in this assignment (20%\*4=80%) of the grade for this assignment. You should only use data **from year 2018** for your analysis -- this is important!
# 
# ## Notes
# 
# 1. Do not include data about the MLS or CFL in any of the work you are doing, we're only interested in the Big 4 in this assignment.
# 2. I highly suggest that you first tackle the four correlation questions in order, as they are all similar and worth the majority of grades for this assignment. This is by design!
# 3. It's fair game to talk with peers about high level strategy as well as the relationship between metropolitan areas and sports teams. However, do not post code solving aspects of the assignment (including such as dictionaries mapping areas to teams, or regexes which will clean up names).
# 4. There may be more teams than the assert statements test, remember to collapse multiple teams in one city into a single value!

# ## Question 1
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NHL** using **2018** data.

# In[94]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re



def nhl_correlation(): 
    nhl_df=pd.read_csv("assets/nhl.csv")
    cities=pd.read_html("assets/wikipedia_data.html", na_values=" ")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities = cities.rename(columns={"Population (2016 est.)[8]":"population"})
    cities.replace(to_replace="\[[\w ]*\]$",value="",regex=True ,inplace=True) 
    nhl_df = nhl_df.drop([0,9,18,26])
    cities = cities.drop([14,15,18,19,20,21,23,24,25,27,28,32,33,38,40,41,42,44,45,46,48,49,50])
    #nhl_df.replace(to_replace="[\w]*$",value="",regex=True ,inplace=True)
    lst = []
    for i in nhl_df["team"]:
        i=i.split('*')
        lst.append(i[0])
    nhl_df["team"] = lst
    
    nhl_df = nhl_df[0:31]
    nhl_df["team_area"] = nhl_df["team"]
    nhl_df["team_area"] = nhl_df["team_area"].map({"Tampa Bay Lightning":"Tampa Bay Area",
     'Boston Bruins':'Boston',
     'Toronto Maple Leafs':'Toronto',
     'Florida Panthers':'Miami–Fort Lauderdale',
     'Detroit Red Wings':'Detroit',
     'Montreal Canadiens':'Montreal',
     'Ottawa Senators':'Ottawa',
     'Buffalo Sabres':'Buffalo',
     'Washington Capitals':'Washington, D.C.',
     'Pittsburgh Penguins':'Pittsburgh',
     'Philadelphia Flyers':'Philadelphia',
     'Columbus Blue Jackets':'Columbus',
     'New Jersey Devils':'New York City',
     'Carolina Hurricanes':'Raleigh',
     'New York Islanders':'New York City',
     'New York Rangers':'New York City',
     'Nashville Predators':'Nashville',
     'Winnipeg Jets':'Winnipeg',
     'Minnesota Wild':'Minneapolis–Saint Paul',
     'Colorado Avalanche':'Denver',
     'St. Louis Blues':'St. Louis',
     'Dallas Stars':'Dallas–Fort Worth',
     'Chicago Blackhawks':'Chicago',
     'Vegas Golden Knights':'Las Vegas',
     'Anaheim Ducks':'Los Angeles',
     'San Jose Sharks':'San Francisco Bay Area',
     'Los Angeles Kings':'Los Angeles',
     'Calgary Flames':'Calgary',
     "Edmonton Oilers":"Edmonton",
     "Vancouver Canucks":"Vancouver",
     "Arizona Coyotes":"Phoenix"})
    
    
    df = pd.merge(nhl_df,cities, left_on= "team_area", right_on= "Metropolitan area")
    df = df[["team","W","L","Metropolitan area","population"]]
    df["W"] = pd.to_numeric(df["W"])
    df["L"] = pd.to_numeric(df["L"])
    df["population"] = pd.to_numeric(df["population"])

    df["w/l"] = df["W"]/(df["L"]+df["W"])
    df = df.groupby("Metropolitan area").mean()
    df = df.reset_index()
    #return (df)
    population_by_region = df["population"] # pass in metropolitan area population from cities
    win_loss_by_region = df["w/l"] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
    
    #return len(win_loss_by_region)
    answer =  stats.pearsonr(population_by_region, win_loss_by_region)[0]
    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    return (answer)



nhl_correlation()


# In[ ]:





# ## Question 2
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NBA** using **2018** data.

# In[38]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def nba_correlation():
    nba_df=pd.read_csv("assets/nba.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities = cities.rename(columns={"Population (2016 est.)[8]":"population"})
    cities.replace(to_replace="\[[\w ]*\]$",value="",regex=True ,inplace=True) 
    cities = cities.drop([16,17,19,20,21,22,23,26,29,30,31,34,35,36,37,39,40,43,44,47,48,49,50])
    lst = []
    for i in nba_df["team"]:
        i=i.split('*')
        lst.append(i[0])
    nba_df["team"] = lst
    
    lstt=[]
    for i in nba_df["team"]:
        i=i.split("(")
        lstt.append(i[0])
    nba_df["team"]=lstt
    
    lsttt=[]
    for i in nba_df["team"]:
        i = i.replace(u'\xa0', u' ')
        i=i.rstrip()
        lsttt.append(i)
    nba_df["team"]=lsttt  
    nba_df=nba_df[:30]
    
    nba_df["team_area"] = nba_df["team"]
    nba_df["team_area"] = nba_df["team_area"].map({"Toronto Raptors":"Toronto",
                                                  "Boston Celtics":"Boston",
                                                  "Philadelphia 76ers":"Philadelphia",
                                                  "Cleveland Cavaliers":"Cleveland",
                                                  "Indiana Pacers":"Indianapolis",
                                                  "Miami Heat":"Miami–Fort Lauderdale",
                                                  "Milwaukee Bucks":"Milwaukee",
                                                  "Washington Wizards":"Washington, D.C.",
                                                  "Detroit Pistons":"Detroit",
                                                  "Charlotte Hornets":"Charlotte",
                                                  "New York Knicks":"New York City",
                                                  "Brooklyn Nets":"New York City",
                                                  "Chicago Bulls":"Chicago",
                                                  "Orlando Magic":"Orlando",
                                                  "Atlanta Hawks":"Atlanta",
                                                  "Houston Rockets":"Houston",
                                                   "Golden State Warriors":"San Francisco Bay Area",
                                                   "Portland Trail Blazers":"Portland",
                                                   "Oklahoma City Thunder":"Oklahoma City",
                                                   "Utah Jazz":"Salt Lake City",
                                                   "New Orleans Pelicans":"New Orleans",
                                                   "San Antonio Spurs":"San Antonio",
                                                   "Minnesota Timberwolves":"Minneapolis–Saint Paul",
                                                   "Denver Nuggets":"Denver",
                                                   "Los Angeles Clippers":"Los Angeles",
                                                   "Los Angeles Lakers":"Los Angeles",
                                                   "Sacramento Kings":"Sacramento",
                                                   "Dallas Mavericks":"Dallas–Fort Worth",
                                                   "Memphis Grizzlies":"Memphis",
                                                   "Phoenix Suns":"Phoenix"})
    
    #return(nba_df)
    df = pd.merge(nba_df,cities, left_on="team_area", right_on="Metropolitan area")
    df["W"] = pd.to_numeric(df["W"])
    df["L"] = pd.to_numeric(df["L"])
    df["population"] = pd.to_numeric(df["population"])
    df = df[["team","W","L","Metropolitan area","population"]]  

    df["w/l"] = df["W"]/(df["L"]+df["W"])
    df = df.groupby("Metropolitan area").mean().reset_index()
    
    #return (df)
    population_by_region = df["population"] # pass in metropolitan area population from cities
    win_loss_by_region = df["w/l"] # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]
    #return (population_by_region)
    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
    
    
nba_correlation()


# In[ ]:





# ## Question 3
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **MLB** using **2018** data.

# In[104]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re



def mlb_correlation(): 
    mlb_df=pd.read_csv("assets/mlb.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities = cities.rename(columns={"Population (2016 est.)[8]":"population"})
    cities.replace(to_replace="\[[\w ]*\]$",value="",regex=True ,inplace=True)
    cities=cities.drop([24,25,26,28,29,30,31,32,33,34,35,36,37,38,39,41,42,43,44,45,46,47,48,49,50])
    mlb_df=mlb_df[0:30]
    mlb_df["team_area"]=mlb_df["team"]
    mlb_df["team_area"]=mlb_df["team_area"].map({"Boston Red Sox":"Boston",
                                                "New York Yankees":"New York City",
                                                "Tampa Bay Rays":"Tampa Bay Area",
                                                "Toronto Blue Jays":"Toronto",
                                                "Baltimore Orioles":"Baltimore",
                                                "Cleveland Indians":"Cleveland",
                                                "Minnesota Twins":"Minneapolis–Saint Paul",
                                                "Detroit Tigers":"Detroit",
                                                "Chicago White Sox":"Chicago",
                                                "Kansas City Royals":"Kansas City",
                                                "Houston Astros":"Houston",
                                                "Oakland Athletics":"San Francisco Bay Area",
                                                "Seattle Mariners":"Seattle",
                                                "Los Angeles Angels":"Los Angeles",
                                                "Texas Rangers":"Dallas–Fort Worth",
                                                "Atlanta Braves":"Atlanta",
                                                "Washington Nationals":"Washington, D.C.",
                                                "Philadelphia Phillies":"Philadelphia",
                                                "New York Mets":"New York City",
                                                "Miami Marlins":"Miami–Fort Lauderdale",
                                                "Milwaukee Brewers":"Milwaukee",
                                                "Chicago Cubs":"Chicago",
                                                "St. Louis Cardinals":"St. Louis",
                                                "Pittsburgh Pirates":"Pittsburgh",
                                                "Cincinnati Reds":"Cincinnati",
                                                "Los Angeles Dodgers":"Los Angeles",
                                                "Colorado Rockies":"Denver",
                                                "Arizona Diamondbacks":"Phoenix",
                                                "San Francisco Giants":"San Francisco Bay Area",
                                                "San Diego Padres":"San Diego"})
    
    df = pd.merge(mlb_df,cities, left_on="team_area", right_on="Metropolitan area")
    df["W"] = pd.to_numeric(df["W"])
    df["L"] = pd.to_numeric(df["L"])
    df["population"] = pd.to_numeric(df["population"])
    df = df[["team","W","L","Metropolitan area","population"]]  
    
    df["w/l"] = df["W"]/(df["L"]+df["W"])
    df = df.groupby("Metropolitan area").mean().reset_index()
    
    
    #return(df)
    
    population_by_region = df["population"] # pass in metropolitan area population from cities
    win_loss_by_region = df["w/l"] # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]



mlb_correlation()


# In[ ]:





# ## Question 4
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NFL** using **2018** data.

# In[108]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re



def nfl_correlation(): 
    nfl_df=pd.read_csv("assets/nfl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities = cities.rename(columns={"Population (2016 est.)[8]":"population"})
    cities.replace(to_replace="\[[\w ]*\]$",value="",regex=True ,inplace=True)
    cities=cities.drop([13,22,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,45,46,47,49,50])
    nfl_df=nfl_df.drop([0,5,10,15,20,25,30,35]).reset_index()

    nfl_df=nfl_df[0:32]
    lst = []
    for i in nfl_df["team"]:
        i=i.split('*')
        lst.append(i[0])
    nfl_df["team"] = lst
    lstt = []
    for i in nfl_df["team"]:
        i=i.split('+')
        lstt.append(i[0])
    nfl_df["team"] = lstt
    
    nfl_df["team_area"]=nfl_df["team"]
    nfl_df["team_area"]=nfl_df["team_area"].map({"New England Patriots":"Boston",
                                                "Miami Dolphins":"Miami–Fort Lauderdale",
                                                "Buffalo Bills":"Buffalo",
                                                "New York Jets":"New York City",
                                                "Baltimore Ravens":"Baltimore",
                                                "Pittsburgh Steelers":"Pittsburgh",
                                                "Cleveland Browns":"Cleveland",
                                                "Cincinnati Bengals":"Cincinnati",
                                                "Houston Texans":"Houston",
                                                "Indianapolis Colts":"Indianapolis",
                                                "Tennessee Titans":"Nashville",
                                                "Jacksonville Jaguars":"Jacksonville",
                                                "Kansas City Chiefs":"Kansas City",
                                                "Los Angeles Chargers":"Los Angeles",
                                                "Denver Broncos":"Denver",
                                                "Oakland Raiders":"Las Vegas",
                                                "Dallas Cowboys":"Dallas–Fort Worth",
                                                "Philadelphia Eagles":"Philadelphia",
                                                "Washington Redskins":"Washington, D.C.",
                                                "New York Giants":"New York City",
                                                "Chicago Bears":"Chicago",
                                                "Minnesota Vikings":"Minneapolis–Saint Paul",
                                                "Green Bay Packers":"Green Bay",
                                                "Detroit Lions":"Detroit",
                                                "New Orleans Saints":"New Orleans",
                                                "Carolina Panthers":"Charlotte",
                                                "Atlanta Falcons":"Atlanta",
                                                "Tampa Bay Buccaneers":"Tampa Bay Area",
                                                "Los Angeles Rams":"Los Angeles",
                                                "Seattle Seahawks":"Seattle",
                                                "San Francisco 49ers":"San Francisco Bay Area",
                                                "Arizona Cardinals":"Phoenix"})
    
    df = pd.merge(nfl_df,cities, left_on="team_area", right_on="Metropolitan area")
    df["W"] = pd.to_numeric(df["W"])
    df["L"] = pd.to_numeric(df["L"])
    df["population"] = pd.to_numeric(df["population"])
    df = df[["team","W","L","Metropolitan area","population"]] 
    df["w/l"] = df["W"]/(df["L"]+df["W"])
    df = df.groupby("Metropolitan area").mean().reset_index()
    #return(df)
    
    
    
    population_by_region = df["population"] # pass in metropolitan area population from cities
    win_loss_by_region = df["w/l"] # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"
    answer =stats.pearsonr(population_by_region, win_loss_by_region)
    return (answer)[0]


nfl_correlation()


# In[ ]:





# ## Question 5
# In this question I would like you to explore the hypothesis that **given that an area has two sports teams in different sports, those teams will perform the same within their respective sports**. How I would like to see this explored is with a series of paired t-tests (so use [`ttest_rel`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html)) between all pairs of sports. Are there any sports where we can reject the null hypothesis? Again, average values where a sport has multiple teams in one region. Remember, you will only be including, for each sport, cities which have teams engaged in that sport, drop others as appropriate. This question is worth 20% of the grade for this assignment.

# In[2]:


def nfldf():
    nfl_df=pd.read_csv("assets/nfl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities = cities.rename(columns={"Population (2016 est.)[8]":"population"})
    cities.replace(to_replace="\[[\w ]*\]$",value="",regex=True ,inplace=True)
    cities=cities.drop([13,22,27,30,31,32,33,34,35,36,37,38,39,40,41,42,43,45,46,47,49,50])
    nfl_df=nfl_df.drop([0,5,10,15,20,25,30,35]).reset_index()

    nfl_df=nfl_df[0:32]
    lst = []
    for i in nfl_df["team"]:
        i=i.split('*')
        lst.append(i[0])
    nfl_df["team"] = lst
    lstt = []
    for i in nfl_df["team"]:
        i=i.split('+')
        lstt.append(i[0])
    nfl_df["team"] = lstt
    
    nfl_df["team_area"]=nfl_df["team"]
    nfl_df["team_area"]=nfl_df["team_area"].map({"New England Patriots":"Boston",
                                                "Miami Dolphins":"Miami–Fort Lauderdale",
                                                "Buffalo Bills":"Buffalo",
                                                "New York Jets":"New York City",
                                                "Baltimore Ravens":"Baltimore",
                                                "Pittsburgh Steelers":"Pittsburgh",
                                                "Cleveland Browns":"Cleveland",
                                                "Cincinnati Bengals":"Cincinnati",
                                                "Houston Texans":"Houston",
                                                "Indianapolis Colts":"Indianapolis",
                                                "Tennessee Titans":"Nashville",
                                                "Jacksonville Jaguars":"Jacksonville",
                                                "Kansas City Chiefs":"Kansas City",
                                                "Los Angeles Chargers":"Los Angeles",
                                                "Denver Broncos":"Denver",
                                                "Oakland Raiders":"Las Vegas",
                                                "Dallas Cowboys":"Dallas–Fort Worth",
                                                "Philadelphia Eagles":"Philadelphia",
                                                "Washington Redskins":"Washington, D.C.",
                                                "New York Giants":"New York City",
                                                "Chicago Bears":"Chicago",
                                                "Minnesota Vikings":"Minneapolis–Saint Paul",
                                                "Green Bay Packers":"Green Bay",
                                                "Detroit Lions":"Detroit",
                                                "New Orleans Saints":"New Orleans",
                                                "Carolina Panthers":"Charlotte",
                                                "Atlanta Falcons":"Atlanta",
                                                "Tampa Bay Buccaneers":"Tampa Bay Area",
                                                "Los Angeles Rams":"Los Angeles",
                                                "Seattle Seahawks":"Seattle",
                                                "San Francisco 49ers":"San Francisco Bay Area",
                                                "Arizona Cardinals":"Phoenix"})
    
    nfldf = pd.merge(nfl_df,cities, left_on="team_area", right_on="Metropolitan area")
    nfldf["W"] = pd.to_numeric(nfldf["W"])
    nfldf["L"] = pd.to_numeric(nfldf["L"])
    nfldf["population"] = pd.to_numeric(nfldf["population"])
    nfldf = nfldf[["team","W","L","Metropolitan area","population"]] 
    nfldf["w/l"] = nfldf["W"]/(nfldf["L"]+nfldf["W"])
    nfldf = nfldf.groupby("Metropolitan area").mean().reset_index()
    return(nfldf)





def nbadf():
    nba_df=pd.read_csv("assets/nba.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities = cities.rename(columns={"Population (2016 est.)[8]":"population"})
    cities.replace(to_replace="\[[\w ]*\]$",value="",regex=True ,inplace=True) 
    cities = cities.drop([16,17,19,20,21,22,23,26,29,30,31,34,35,36,37,39,40,43,44,47,48,49,50])
    lst = []
    for i in nba_df["team"]:
        i=i.split('*')
        lst.append(i[0])
    nba_df["team"] = lst
    
    lstt=[]
    for i in nba_df["team"]:
        i=i.split("(")
        lstt.append(i[0])
    nba_df["team"]=lstt
    
    lsttt=[]
    for i in nba_df["team"]:
        i = i.replace(u'\xa0', u' ')
        i=i.rstrip()
        lsttt.append(i)
    nba_df["team"]=lsttt  
    nba_df=nba_df[:30]
    
    nba_df["team_area"] = nba_df["team"]
    nba_df["team_area"] = nba_df["team_area"].map({"Toronto Raptors":"Toronto",
                                                  "Boston Celtics":"Boston",
                                                  "Philadelphia 76ers":"Philadelphia",
                                                  "Cleveland Cavaliers":"Cleveland",
                                                  "Indiana Pacers":"Indianapolis",
                                                  "Miami Heat":"Miami–Fort Lauderdale",
                                                  "Milwaukee Bucks":"Milwaukee",
                                                  "Washington Wizards":"Washington, D.C.",
                                                  "Detroit Pistons":"Detroit",
                                                  "Charlotte Hornets":"Charlotte",
                                                  "New York Knicks":"New York City",
                                                  "Brooklyn Nets":"New York City",
                                                  "Chicago Bulls":"Chicago",
                                                  "Orlando Magic":"Orlando",
                                                  "Atlanta Hawks":"Atlanta",
                                                  "Houston Rockets":"Houston",
                                                   "Golden State Warriors":"San Francisco Bay Area",
                                                   "Portland Trail Blazers":"Portland",
                                                   "Oklahoma City Thunder":"Oklahoma City",
                                                   "Utah Jazz":"Salt Lake City",
                                                   "New Orleans Pelicans":"New Orleans",
                                                   "San Antonio Spurs":"San Antonio",
                                                   "Minnesota Timberwolves":"Minneapolis–Saint Paul",
                                                   "Denver Nuggets":"Denver",
                                                   "Los Angeles Clippers":"Los Angeles",
                                                   "Los Angeles Lakers":"Los Angeles",
                                                   "Sacramento Kings":"Sacramento",
                                                   "Dallas Mavericks":"Dallas–Fort Worth",
                                                   "Memphis Grizzlies":"Memphis",
                                                   "Phoenix Suns":"Phoenix"})
    
    nbadf = pd.merge(nba_df,cities, left_on="team_area", right_on="Metropolitan area")
    nbadf["W"] = pd.to_numeric(nbadf["W"])
    nbadf["L"] = pd.to_numeric(nbadf["L"])
    nbadf["population"] = pd.to_numeric(nbadf["population"])
    nbadf = nbadf[["team","W","L","Metropolitan area","population"]]  

    nbadf["w/l"] = nbadf["W"]/(nbadf["L"]+nbadf["W"])
    nbadf = nbadf.groupby("Metropolitan area").mean().reset_index()
    
    return (nbadf)



def nhldf():
    nhl_df=pd.read_csv("assets/nhl.csv")
    cities=pd.read_html("assets/wikipedia_data.html", na_values=" ")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities = cities.rename(columns={"Population (2016 est.)[8]":"population"})
    cities.replace(to_replace="\[[\w ]*\]$",value="",regex=True ,inplace=True) 
    nhl_df = nhl_df.drop([0,9,18,26])
    cities = cities.drop([14,15,18,19,20,21,23,24,25,27,28,32,33,38,40,41,42,44,45,46,48,49,50])
    #nhl_df.replace(to_replace="[\w]*$",value="",regex=True ,inplace=True)
    lst = []
    for i in nhl_df["team"]:
        i=i.split('*')
        lst.append(i[0])
    nhl_df["team"] = lst
    
    nhl_df = nhl_df[0:31]
    nhl_df["team_area"] = nhl_df["team"]
    nhl_df["team_area"] = nhl_df["team_area"].map({"Tampa Bay Lightning":"Tampa Bay Area",
     "Boston Bruins":"Boston",
     'Toronto Maple Leafs':'Toronto',
     'Florida Panthers':'Miami–Fort Lauderdale',
     'Detroit Red Wings':'Detroit',
     'Montreal Canadiens':'Montreal',
     'Ottawa Senators':'Ottawa',
     'Buffalo Sabres':'Buffalo',
     'Washington Capitals':'Washington, D.C.',
     'Pittsburgh Penguins':'Pittsburgh',
     'Philadelphia Flyers':'Philadelphia',
     'Columbus Blue Jackets':'Columbus',
     'New Jersey Devils':'New York City',
     'Carolina Hurricanes':'Raleigh',
     'New York Islanders':'New York City',
     'New York Rangers':'New York City',
     'Nashville Predators':'Nashville',
     'Winnipeg Jets':'Winnipeg',
     'Minnesota Wild':'Minneapolis–Saint Paul',
     'Colorado Avalanche':'Denver',
     'St. Louis Blues':'St. Louis',
     'Dallas Stars':'Dallas–Fort Worth',
     'Chicago Blackhawks':'Chicago',
     'Vegas Golden Knights':'Las Vegas',
     'Anaheim Ducks':'Los Angeles',
     'San Jose Sharks':'San Francisco Bay Area',
     'Los Angeles Kings':'Los Angeles',
     'Calgary Flames':'Calgary',
     "Edmonton Oilers":"Edmonton",
     "Vancouver Canucks":"Vancouver",
     "Arizona Coyotes":"Phoenix"})
    
    
    df = pd.merge(nhl_df,cities, left_on= "team_area", right_on= "Metropolitan area")
    df = df[["team","W","L","Metropolitan area","population"]]
    df["W"] = pd.to_numeric(df["W"])
    df["L"] = pd.to_numeric(df["L"])
    df["population"] = pd.to_numeric(df["population"])

    df["w/l"] = df["W"]/(df["L"]+df["W"])
    df = df.groupby("Metropolitan area").mean()
    df = df.reset_index()
    return (df)




def mlbdf():
    mlb_df=pd.read_csv("assets/mlb.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities = cities.rename(columns={"Population (2016 est.)[8]":"population"})
    cities.replace(to_replace="\[[\w ]*\]$",value="",regex=True ,inplace=True)
    cities=cities.drop([24,25,26,28,29,30,31,32,33,34,35,36,37,38,39,41,42,43,44,45,46,47,48,49,50])
    mlb_df=mlb_df[0:30]
    mlb_df["team_area"]=mlb_df["team"]
    mlb_df["team_area"]=mlb_df["team_area"].map({"Boston Red Sox":"Boston",
                                                "New York Yankees":"New York City",
                                                "Tampa Bay Rays":"Tampa Bay Area",
                                                "Toronto Blue Jays":"Toronto",
                                                "Baltimore Orioles":"Baltimore",
                                                "Cleveland Indians":"Cleveland",
                                                "Minnesota Twins":"Minneapolis–Saint Paul",
                                                "Detroit Tigers":"Detroit",
                                                "Chicago White Sox":"Chicago",
                                                "Kansas City Royals":"Kansas City",
                                                "Houston Astros":"Houston",
                                                "Oakland Athletics":"San Francisco Bay Area",
                                                "Seattle Mariners":"Seattle",
                                                "Los Angeles Angels":"Los Angeles",
                                                "Texas Rangers":"Dallas–Fort Worth",
                                                "Atlanta Braves":"Atlanta",
                                                "Washington Nationals":"Washington, D.C.",
                                                "Philadelphia Phillies":"Philadelphia",
                                                "New York Mets":"New York City",
                                                "Miami Marlins":"Miami–Fort Lauderdale",
                                                "Milwaukee Brewers":"Milwaukee",
                                                "Chicago Cubs":"Chicago",
                                                "St. Louis Cardinals":"St. Louis",
                                                "Pittsburgh Pirates":"Pittsburgh",
                                                "Cincinnati Reds":"Cincinnati",
                                                "Los Angeles Dodgers":"Los Angeles",
                                                "Colorado Rockies":"Denver",
                                                "Arizona Diamondbacks":"Phoenix",
                                                "San Francisco Giants":"San Francisco Bay Area",
                                                "San Diego Padres":"San Diego"})
    
    df = pd.merge(mlb_df,cities, left_on="team_area", right_on="Metropolitan area")
    df["W"] = pd.to_numeric(df["W"])
    df["L"] = pd.to_numeric(df["L"])
    df["population"] = pd.to_numeric(df["population"])
    df = df[["team","W","L","Metropolitan area","population"]]  
    
    df["w/l"] = df["W"]/(df["L"]+df["W"])
    df = df.groupby("Metropolitan area").mean().reset_index()
    
    
    return(df)
    
    
    


# In[3]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def sports_team_performance():
    mlb_df = mlbdf()
    nhl_df = nhldf()
    nba_df = nbadf()
    nfl_df = nfldf()
    cities = pd.read_html("assets/wikipedia_data.html")[1]
    cities = cities.iloc[:-1,[0,3,5,6,7,8]]
    cities = cities.rename(columns={"Population (2016 est.)[8]":"population"})
    cities.replace(to_replace="\[[\w ]*\]$",value="",regex=True ,inplace=True)
    #return(cities)
    # Note: p_values is a full dataframe, so df.loc["NFL","NBA"] should be the same as df.loc["NBA","NFL"] and
    # df.loc["NFL","NFL"] should return np.nan
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame({k:np.nan for k in sports}, index=sports)
    
    for row in sports:
        for column in sports:
            if row != column:
                if row == "NFL":
                    rowvalue = nfl_df
                    if column == "NBA":
                        colvalue = nba_df
                        merge = pd.merge(rowvalue,colvalue,on="Metropolitan area")
                        p_values.loc[row, column]=stats.ttest_rel(merge["w/l_x"],merge["w/l_y"])[1]
                    if column == "NHL":
                        colvalue = nhl_df
                        merge = pd.merge(rowvalue,colvalue,on="Metropolitan area")
                        p_values.loc[row, column]=stats.ttest_rel(merge["w/l_x"],merge["w/l_y"])[1]
                    if column == "MLB":
                        colvalue = mlb_df
                        merge = pd.merge(rowvalue,colvalue,on="Metropolitan area")
                        p_values.loc[row, column]=stats.ttest_rel(merge["w/l_x"],merge["w/l_y"])[1]
                if row == "NBA":
                    rowvalue = nba_df
                    if column == "NFL":
                        colvalue = nfl_df
                        merge = pd.merge(rowvalue,colvalue,on="Metropolitan area")
                        p_values.loc[row, column]=stats.ttest_rel(merge["w/l_x"],merge["w/l_y"])[1]
                    if column == "NHL":
                        colvalue = nhl_df
                        merge = pd.merge(rowvalue,colvalue,on="Metropolitan area")
                        p_values.loc[row, column]=stats.ttest_rel(merge["w/l_x"],merge["w/l_y"])[1]
                    if column == "MLB":
                        colvalue = mlb_df
                        merge = pd.merge(rowvalue,colvalue, on="Metropolitan area")
                        p_values.loc[row, column]=stats.ttest_rel(merge["w/l_x"],merge["w/l_y"])[1]
                if row == "NHL":
                    rowvalue = nhl_df
                    if column == "NFL":
                        colvalue = nfl_df
                        merge = pd.merge(rowvalue,colvalue, on="Metropolitan area")
                        p_values.loc[row, column]=stats.ttest_rel(merge["w/l_x"],merge["w/l_y"])[1]
                    if column == "NBA":
                        colvalue = nba_df
                        merge = pd.merge(rowvalue,colvalue, on="Metropolitan area")
                        p_values.loc[row, column]=stats.ttest_rel(merge["w/l_x"],merge["w/l_y"])[1]
                    if column == "MLB":
                        colvalue = mlb_df
                        merge = pd.merge(rowvalue,colvalue, on="Metropolitan area")
                        p_values.loc[row, column]=stats.ttest_rel(merge["w/l_x"],merge["w/l_y"])[1]
                if row == "MLB":
                    rowvalue = mlb_df
                    if column == "NFL":
                        colvalue = nfl_df
                        merge = pd.merge(rowvalue,colvalue, on="Metropolitan area")
                        p_values.loc[row, column]=stats.ttest_rel(merge["w/l_x"],merge["w/l_y"])[1]
                    if column == "NBA":
                        colvalue = nba_df
                        merge = pd.merge(rowvalue,colvalue, on="Metropolitan area")
                        p_values.loc[row, column]=stats.ttest_rel(merge["w/l_x"],merge["w/l_y"])[1]
                    if column == "NHL":
                        colvalue = nhl_df
                        merge = pd.merge(rowvalue,colvalue, on="Metropolitan area")
                        p_values.loc[row, column] = stats.ttest_rel(merge["w/l_x"],merge["w/l_y"])[1]
                    
    
    
    
    assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    return p_values
    
    
sports_team_performance()


# In[ ]:




