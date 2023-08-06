""" 
Supplementary functions for TBML (bettingmodels) app

"""

import pandas as pd
import datetime
from bs4 import BeautifulSoup
import requests
import numpy as np

def _is_player_name(tag):
    if tag.name=="h3":
        return True
    return False

## Check if TE tag on player page contains player's nationality

def _is_player_country(tag):
    if tag.has_attr("class"):
        if tag["class"]==["date"]:
            if list(tag.descendants)[0][:7]=="Country":
                return True
    return False

## Check if TE tag on player page contains player's birth date

def _is_player_birthdate(tag):
    if tag.has_attr("class"):
        if tag["class"]==["date"]:
            if list(tag.descendants)[0][:3]=="Age":
                return True
    return False

def _is_player_antropometrics(tag):
    if tag.has_attr("class"):
        if tag["class"]==["date"]:
            if list(tag.descendants)[0][:6]=="Height":
                return True
    return False

## Check if TE tag on player page contains player's gender

def _is_player_gender(tag):
    if tag.has_attr("class"):
        if tag["class"]==["date"]:
            if list(tag.descendants)[0][:3]=="Sex":
                return True
    return False

## Check if TE tag on player page contains player's preferred hand

def _is_player_handed(tag):
    if tag.has_attr("class"):
        if tag["class"]==["date"]:
            if list(tag.descendants)[0][:5]=="Plays":
                return True
    return False

## Check if TE tag on results page contains tournament name

def _is_tourney(tag):
    if tag.has_attr("class") and tag.has_attr("colspan"):
        if tag["colspan"]=="2":
            return True
    return False

## Check if TE tag on results page contains match time

def _is_match_time(tag):
    if tag.has_attr("class"):
        if tag["class"]==['first', 'time']:
            return True
    return False

## Check if TE tag on results page contains link to match details

def _is_link_matchdetails(tag):
    if not tag.has_attr("class") and tag.has_attr("rowspan"):
        if tag["rowspan"]=="2":
            return True
    return False

## Check if TE tag on results page contains player ID

def _is_player(tag):
    if tag.has_attr("class") and not tag.has_attr("colspan"):
        if tag["class"]==['t-name']:
            return True
    return False

## Check if TE tag on results page contains match result

def _is_result(tag):
    if tag.has_attr("class"):
        if tag["class"]==['result']:
            return True
    return False

## Check if TE tag on results page contains match score

def _is_score(tag):
    if tag.has_attr("class"):
        if tag["class"]==['score']:
            return True
    return False

def _is_currentmatches_table(tag, date):
    date_text=date.strftime("%d. %m. %Y")
    try:
        tag_text = list(list(list((list(tag.descendants)[1]).
                                        descendants)[1].
                                        descendants)[0].descendants)[0]
        if date_text==tag_text:
            return True
        else:
            return False
    except AttributeError:
        return False

## Check if TE tag on match page contains home odds 

def _is_odds_home(tag):
    if tag.name=="td":
        if tag.has_attr("class"):
            if 'k1' in tag['class'] and 'deactivated' not in tag['class']:
                if len(tag.find_all("div"))>0:
                    return True
    return False
    
## Check if TE tag on match page contains away odds

def _is_odds_away(tag):
    if tag.name=="td":
        if tag.has_attr("class"):
            if 'k2' in tag['class'] and 'deactivated' not in tag['class']:
                if len(tag.find_all("div"))>0:
                    return True
    return False

## Check if TE tag on match page contains the bookie name

def _is_bookie(tag):
    if tag.name=="td":
            if tag.has_attr('class'):
                if tag['class']==['first', 'tl']:
                    return True
    return False

## Check if TE tag on match page contains odds type (e.g. home-away, handicap)

def _is_odds_type(tag):
    if tag.name=="td":
            if tag.has_attr('colspan'):
                if tag['colspan']=="4":
                    return True
    return False

## Check if TE tag on match page contains average odds (last line of odds table)
        
def _is_average_odds(tag):
    if tag.name=="td":
        if list(tag.descendants)[0]=="Average odds":
            return True
    return False

## Check if TE tag on match page contains odds value (e.g. 1.50)

def _is_odds_value(tag):
    if tag.name=="td":
        if tag.has_attr("class"):
            if tag['class']==['value']:
                return True
    return False
   
## Switch Player 1 and Player 2 data in Matches data frame including
## corresponding scores
## Input: data frame containing matches
## Output: data frame containing permuted matches
    
def _permute_matches(df):
    df['permute']=np.random.choice([True,False], df.shape[0])
    rows_to_permute=df[df['permute']==True]
    counter=0
    for index in list(rows_to_permute.index.values):
        df.loc[index,['Player1','Player2']] \
        = df.loc[index,['Player2','Player1']].values
        df.loc[index,['SetsPlayer1','SetsPlayer2']] \
        = df.loc[index,['SetsPlayer2','SetsPlayer1']].values
        df.loc[index,['Set1Player1','Set1Player2']] \
        = df.loc[index,['Set1Player2','Set1Player1']].values
        df.loc[index,['Set2Player1','Set2Player2']] \
        = df.loc[index,['Set2Player2','Set2Player1']].values
        df.loc[index,['Set3Player1','Set3Player2']] \
        = df.loc[index,['Set3Player2','Set3Player1']].values
        df.loc[index,['Set4Player1','Set4Player2']] \
        = df.loc[index,['Set4Player2','Set4Player1']].values
        df.loc[index,['Set5Player1','Set5Player2']] \
        = df.loc[index,['Set5Player2','Set5Player1']].values
        df.loc[index,['Result']]=-df.loc[index,['Result']].values+3
        df.loc[index,['Retired']]=df.loc[index,['Retired']].values/2
        counter+=1
    return df

## Process matches by calculating games, tiebreaks, result and retired values
    
def processing1(df_matches):
    
    # define tournaments with best-of-five
    fivesetters=["australian-open-atp-single",
                 "french-open-atp-single",
                 "wimbledon-atp-single",
                 "us-open-atp-single",
                 "davis-cup-atp-single",
                 "olympics-london-atp-single",
                 "olympics-beijing-atp-single",
                 "olympics-athens-atp-single",
                 "olympics-rio-de-janeiro-atp-single"]
    
    # determine Result and Retired values
    df_matches['Result']=-((df_matches['SetsPlayer1']>df_matches['SetsPlayer2'])*1-2)
    df_matches['Retired']=np.where(df_matches[['SetsPlayer1','SetsPlayer2']].max(axis=1)<2,2,0)
    
    # permute matches
    df_matches = _permute_matches(df_matches)
    df_matches = df_matches.drop("permute",axis=1)    
    print ("Permutation completed")


    # calculate GamesOverallPlayerX    
    df_matches['GamesOverallPlayer1']=df_matches[['Set1Player1',
              'Set2Player1','Set3Player1','Set4Player1',
              'Set5Player1']].sum(axis=1)
    df_matches['GamesOverallPlayer2']=df_matches[['Set1Player2',
              'Set2Player2','Set3Player2','Set4Player2',
              'Set5Player2']].sum(axis=1)
    
    # calculate TiebreaksPlayerX
    df_matches['TiebreaksPlayer1']=np.where(
            np.logical_and(
                    df_matches['Set1Player1']==7,
                    df_matches['Set1Player2']==6),1,0) \
            + np.where(np.logical_and(
                    df_matches['Set2Player1']==7,
                    df_matches['Set2Player2']==6),1,0) \
                    + np.where(
                            np.logical_and(
                                    df_matches['Set3Player1']==7,
                                    df_matches['Set3Player2']==6),1,0) \
                            + np.where(
                                    np.logical_and(
                                            df_matches['Set4Player1']==7,
                                            df_matches['Set4Player2']==6),1,0) \
                                    + np.where(
                                            np.logical_and(
                                                    df_matches['Set5Player1']==7,
                                                    df_matches['Set5Player2']==6),1,0)
    df_matches['TiebreaksPlayer2']=np.where(
            np.logical_and(
                    df_matches['Set1Player1']==6,
                    df_matches['Set1Player2']==7),1,0) \
            + np.where(np.logical_and(
                    df_matches['Set2Player1']==6,
                    df_matches['Set2Player2']==7),1,0) \
                    + np.where(
                            np.logical_and(
                                    df_matches['Set3Player1']==6,
                                    df_matches['Set3Player2']==7),1,0) \
                            + np.where(
                                    np.logical_and(
                                            df_matches['Set4Player1']==6,
                                            df_matches['Set4Player2']==7),1,0) \
                                    + np.where(
                                            np.logical_and(
                                                    df_matches['Set5Player1']==6,
                                                    df_matches['Set5Player2']==7),1,0)
    
    # calculate GamesPlayerX by subtracting Tiebreaks from GamesOverall
    df_matches['GamesPlayer1']=df_matches['GamesOverallPlayer1'] \
    - df_matches['TiebreaksPlayer1']
    df_matches['GamesPlayer2']=df_matches['GamesOverallPlayer2'] \
    - df_matches['TiebreaksPlayer2']
    
    # handle tiebreak tens
    # identify
    df_matches_tbtens=df_matches[
            df_matches['Retired']==0][
                    (((df_matches['Set3Player1']==10) \
                      | (df_matches['Set3Player2']==10)) \
    | (df_matches['Set3Player1']>10) \
    & (df_matches['Set3Player1'] \
       - df_matches['Set3Player2']==2)) \
    | ((df_matches['Set3Player2']>10) \
       & (df_matches['Set3Player2']-df_matches['Set3Player1']==2))]
    
    # separate from "normal" matches
    df_matches_tbtens=df_matches_tbtens[~df_matches_tbtens['Tourney'].isin(
            fivesetters)]
    
    df_matches_rest=df_matches[
            ~df_matches.index.isin(df_matches_tbtens.index.values)]
    
    # iterate and modify GamesOverall, Games and Tiebreaks
    for index,row in df_matches_tbtens.iterrows():
        
        currentmatch=index
        
        df_matches_tbtens.loc[currentmatch,'GamesPlayer1'] \
        =df_matches_tbtens.loc[currentmatch,'GamesPlayer1'] \
        - df_matches_tbtens.loc[currentmatch,'Set3Player1']
        
        df_matches_tbtens.loc[currentmatch,'GamesPlayer2'] \
        =df_matches_tbtens.loc[currentmatch,'GamesPlayer2'] \
        - df_matches_tbtens.loc[currentmatch,'Set3Player2']
        
        df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer1'] \
        =df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer1'] \
        - df_matches_tbtens.loc[currentmatch,'Set3Player1']
        
        df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer2'] \
        =df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer2'] \
        - df_matches_tbtens.loc[currentmatch,'Set3Player2']
    
        
        df_matches_tbtens.loc[currentmatch,'TiebreaksPlayer1'] \
        = df_matches_tbtens.loc[currentmatch,'TiebreaksPlayer1'] \
        + (df_matches_tbtens.loc[currentmatch,'Set3Player1'] \
         >df_matches_tbtens.loc[currentmatch,'Set3Player2'])
        
        df_matches_tbtens.loc[currentmatch,'TiebreaksPlayer2'] \
        = df_matches_tbtens.loc[currentmatch,'TiebreaksPlayer2'] \
        + (df_matches_tbtens.loc[currentmatch,'Set3Player1'] \
         < df_matches_tbtens.loc[currentmatch,'Set3Player2'])
    
        df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer1'] \
        = df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer1'] \
        + (df_matches_tbtens.loc[currentmatch,'Set3Player1'] \
         >df_matches_tbtens.loc[currentmatch,'Set3Player2'])
        
        df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer2'] \
        = df_matches_tbtens.loc[currentmatch,'GamesOverallPlayer2'] \
        + (df_matches_tbtens.loc[currentmatch,'Set3Player1'] \
         < df_matches_tbtens.loc[currentmatch,'Set3Player2'])
    
    # concatenate back    
    df_matches=pd.concat([df_matches_rest,df_matches_tbtens])
    df_matches=df_matches.sort_values(
            ['DateTime'],ascending=[True])
    
    return df_matches    

## Download player data
## Input: TE player ID
## Output: Dataframe of length 1 containing player data

def download_player(player_id):
    
    # find webpage with player info and convert to BeautifulSoup                                                
    url="http://www.tennisexplorer.com/player/"+player_id
    urlcontents = requests.get(url).text
    soup = BeautifulSoup(urlcontents, "lxml")

    # create dictionary for player data
    current_player={"id_te":player_id}

    # find <td> tag with player data in BeautifulSoup
    # fill current_player with player data 
    playerData=list(soup.find_all(
        "tbody")[0].descendants)[1].find_all("td")[1]

    for tag in playerData:
        if _is_player_name(tag):
            current_player["name"]=list(tag.descendants)[0]

        if _is_player_country(tag):
            current_player["country"]=list(tag.descendants)[0][9:]

        if _is_player_birthdate(tag):
            current_player["birthdate"]=datetime.datetime.strptime(
                list(tag.descendants)[0].split("(")[1].replace(
                        " ","").replace(")",""),
                "%d.%m.%Y").date()
                
        if _is_player_antropometrics(tag):
            try:
                text=list(tag.descendants)[0].split(":")[1]
                hw=[int(s) for s in text.split() if s.isdigit()]
                current_player["height"]=hw[0]
                current_player["weight"]=hw[1]
            except IndexError:
                pass

        if _is_player_gender(tag):
            current_player["gender"]=list(tag.descendants)[0][5:]

        if _is_player_handed(tag):
            current_player["handed"]=list(tag.descendants)[0][7:]

    if not "country" in current_player:
        current_player["country"]=None

    if not "birthdate" in current_player:
        current_player["birthdate"]=None

    if not "handed" in current_player:
        current_player["handed"]=None
        
    if not "height" in current_player:
        current_player["height"]=None
        
    if not "weight" in current_player:
        current_player["weight"]=None

    # convert current_player to Pandas dataframe
    df_currentplayer=pd.DataFrame({'PlayerID':current_player["id_te"],
                                   'Name':current_player["name"],
                                   'Country':current_player["country"],
                                   'Birthdate':current_player["birthdate"],
                                   'Gender':current_player["gender"],
                                   'Handed':current_player["handed"],
                                   'Height':current_player["height"],
                                   'Weight':current_player["weight"]},
                index=['PlayerID'])
    df_currentplayer=df_currentplayer.set_index(['PlayerID'])
    
    return df_currentplayer

## Download tourney data
## Input: TE tourney ID
## Output: Dataframe of length 1 containing player data

def download_tourney(tourney_id,results_type,year):
    
    # convert ATP/WTA to correct url
    if results_type == "atp-single":
        results_type_url="atp-men"
    elif results_type == "wta-single":
        results_type_url = "wta-women"
    
    # find webpage with tourney info and convert to BeautifulSoup 
    url="http://www.tennisexplorer.com/" \
    + tourney_id + "/" \
    + str(year) + "/" \
    + results_type_url 
    
    urlcontents = requests.get(url).text
    tourney_id_composed=tourney_id+"-"+results_type
    
    # catch tournaments without data (e.g. Futures)
    if "Tournament does not exist" in urlcontents:
        df_currenttourney=pd.DataFrame({'TourneyIDComposed':tourney_id_composed,
                                        'TourneyName':tourney_id,
                                        'Gender':results_type_url[4:].replace('e','a'),
                                        'Country':None,
                                        'Year':year,
                                        'Surface':None},
        index=['TourneyIDComposed'])
        df_currenttourney=df_currenttourney.set_index(['TourneyIDComposed'])
        return(df_currenttourney)
    
    soup = BeautifulSoup(urlcontents, "lxml")
    
    # create dictionary for tourney data    
    current_tourney={"id_te":tourney_id_composed,
                     "gender":results_type_url[4:].replace('e','a')}
    
    # find tags with tourney data in BeautifulSoup
    # fill current_tourney with tourney data 
    
    tourney_data1=list(soup.find_all("h1")[0].descendants)[0]
    current_tourney['tourney_name']=tourney_data1[
            :tourney_data1.index("(")-6]
    current_tourney['country']=tourney_data1[
            tourney_data1.index("(")+1:-1]
    
    current_tourney['year']=year
    
    tourney_data2=list(soup.find_all(
            "div", {'class':'box boxBasic lGray'})[1].descendants)[0]
    current_tourney['surface']=tourney_data2.split(',')[-2][1:]
    
    # convert current_tourney to Pandas dataframe
    df_currenttourney=pd.DataFrame({'TourneyIDComposed':current_tourney["id_te"],
                                    'TourneyName':current_tourney["tourney_name"],
                                    'Gender':current_tourney["gender"],
                                    'Country':current_tourney["country"],
                                    'Year':current_tourney['year'],
                                    'Surface':current_tourney["surface"]},
    index=['TourneyIDComposed'])
    df_currenttourney=df_currenttourney.set_index(['TourneyIDComposed'])
    
    return df_currenttourney

## Downloads match results for range of dates
## returns pandas dataframe with match results, updated players and tourneys 
## dataframe
    
## start_date: datetime.datetime object containing first date in date range
## end_date: datetime.datetime object containing last date in date range
## updatePlayers: boolean whether new players should be downloaded
## **kwargs (match_ids, player_ids, tourney_ids): ID lists for matches, 
## players and tourneys in the database  

def download_matches(start_date,
                     end_date,
                     results_type,
                     **kwargs):
    
    # Create list of all dates between start_date and end_date
    
    date_list = [start_date + datetime.timedelta(days=x)
                 for x in range(0, (end_date-start_date).days+1)]

    # Create empty data frames for new results, players, tourneys

    columns_results=['MatchID',
                     'DateTime',
                     'Tourney',
                     'Player1',
                     'Player2',
                     'SetsPlayer1',
                     'SetsPlayer2',
                     'Set1Player1',
                     'Set2Player1',
                     'Set3Player1',
                     'Set4Player1',
                     'Set5Player1',
                     'Set1Player2',
                     'Set2Player2',
                     'Set3Player2',
                     'Set4Player2',
                     'Set5Player2',
                     'finished']
    df_results_new=pd.DataFrame(columns=columns_results)    

    if 'player_ids' in kwargs:
        columns_players=['PlayerID',
                         'Name',
                         'Country',
                         'Birthdate',
                         'Gender',
                         'Handed',
                         'Height',
                         'Weight']
        df_players_new=pd.DataFrame(columns=columns_players)
        df_players_new=df_players_new.set_index(['PlayerID'])

    if 'tourney_ids' in kwargs:
        columns_tourneys=['TourneyIDComposed',
                          'TourneyName',
                          'Gender',
                          'Country',
                          'Year',
                          'Surface']
        df_tourneys_new=pd.DataFrame(columns=columns_tourneys)
        df_tourneys_new=df_tourneys_new.set_index(['TourneyIDComposed'])

    # Iterate through date list

    for currentdate in date_list:
        
        # Create URL, open TE page, create BS object with page contents
        
        url="http://www.tennisexplorer.com/results/?type=" + \
             results_type + \
             "&year=" + str(currentdate.year) + \
             "&month=" + str(currentdate.month) + \
             "&day="+str(currentdate.day)
        urlcontents = requests.get(url).text
        soup = BeautifulSoup(urlcontents, "lxml")

        # Create empty dictionaries/lists for match/tourney details

        current_tourney={}
        current_match={}
        current_match["score_sets"]=[]
        current_match["scores_p1"]=[]
        current_match["scores_p2"]=[]

        # Find results table and all results tags

        resultsTable = soup.find("table", {"class":"result"})
        results_tags = resultsTable.find_all("td")

        # Define variables to open/close match, Player 1/2 scores
        # These variables delineate between single matches/players

        match_open=False
        first_player_open=False
        second_player_open=False
        
        # Iterate through tags in results table

        for tag in results_tags:
            
            # Check if tag contains tourney details and fill current_tourney
            # else branch catches tourneys without hyperlink (<a> tag, e.g. 
            # Futures events)
            
            if _is_tourney(tag):
                if tag.find("a"):
                    current_tourney["url"]=list(tag.descendants)[0]["href"]
                    tid=current_tourney["url"][1:]
                    current_tourney["id"]= tid[:tid.index("/")]                                                                          
                    current_tourney["name"]=list(tag.descendants)[-1]
                else:
                    current_tourney["url"]=None
                    current_tourney["name"]=list(tag.descendants)[-1]
                    current_tourney["id"]=current_tourney["name"].replace(" ","-").lower()
                
                
                current_tourney_id_composed=current_tourney["id"] \
                + "-" + results_type
                currentyear=currentdate.year
                
                # Check if tourney_id exists in database, add to new
                # tourney data frame if missing
                
                if 'tourney_ids' in kwargs:
                    if ((current_tourney_id_composed \
                        not in kwargs['tourney_ids']) \
                        and (current_tourney_id_composed \
                        not in df_tourneys_new.index.unique())):
                        df_t=download_tourney(current_tourney["id"],
                                              results_type,
                                              currentyear)
                        df_tourneys_new=pd.concat([df_tourneys_new, df_t])

            # Check if tag contains match time

            if _is_match_time(tag):

                # Open match and Player 1 with match time tag
                
                match_open=True
                first_player_open=True
                
                # Fill current_match dictionary with current tourney and
                # date/time (23:59 if time is missing)

                current_match["tourney"]=current_tourney
                try:
                    current_match["datetime"]=str(currentdate.year)+"-"\
                                              +str(currentdate.month)+"-"\
                                              +str(currentdate.day)+" "\
                                              +list(tag.descendants)[0][:2]+":"\
                                              +list(tag.descendants)[0][-2:]+":"\
                                              +"0"
                    datetime.datetime.strptime(current_match["datetime"], 
                                               '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    current_match["datetime"]=str(currentdate.year)+"-"\
                                              +str(currentdate.month)+"-"\
                                              +str(currentdate.day)+" "\
                                              +"23:59:00"

            # Exctract match details URL and match ID

            if match_open and _is_link_matchdetails(tag):
                current_match["url"]=list(tag.descendants)[0]["href"]
                current_match["id_te"]=list(tag.descendants)[0]["href"][18:]
                
            if match_open and _is_player(tag):
                
                # Extract Player 1 details
                
                if first_player_open:
                    try:
                        current_match["p1"]={
                            "name":list(tag.descendants)[1],
                            "url":list(tag.descendants)[0]["href"],
                            "id":list(tag.descendants)[0]["href"][8:-1]}
                    except IndexError:
                        current_match["p1"]={
                            "name":list(tag.descendants)[0],
                            "url":None,
                            "id":None}
                
                # Extract Player 2 details
                
                elif second_player_open:
                    try:
                        current_match["p2"]={
                            "name":list(tag.descendants)[1],
                            "url":list(tag.descendants)[0]["href"],
                            "id":list(tag.descendants)[0]["href"][8:-1]}
                    except IndexError:
                        current_match["p2"]={
                            "name":list(tag.descendants)[0],
                            "url":None,
                            "id":None}

            # Extract match result in sets
                
            if match_open and _is_result(tag):
                if list(tag.descendants)[0]=="\xa0":
                    current_match["score_sets"].append(None)
                else:
                    current_match["score_sets"].append(int(list(tag.descendants)[0]))

            # Extract set scores

            try:
            
                if match_open and _is_score(tag):
                    
                    # Extract set scores for Player 1
                    
                    if first_player_open:
                        if list(tag.descendants)[0]=="\xa0":
                            current_match["scores_p1"].append(None)
                        else:
                            current_match["scores_p1"].append(int(list(tag.descendants)[0]))
                    
                    # Extract set scores for Player 2
                    
                    elif second_player_open:
                        if list(tag.descendants)[0]=="\xa0":
                            current_match["scores_p2"].append(None)
                        else:
                            current_match["scores_p2"].append(int(list(tag.descendants)[0]))
                        
            # Open Player 2 when 5 set score tags for Player 1 and fewer than 5
            # set score tags for Player 2 are iterated through

                if match_open and (
                    len(current_match["scores_p1"])>=5 and len(current_match["scores_p2"])<5):
                    first_player_open=False
                    second_player_open=True
    
                # Close Player 2 and match when 5 sets for Player 2 are iterated
                # through
    
                if match_open and (
                    len(current_match["scores_p1"])>=5 and len(current_match["scores_p2"])>=5):
                    second_player_open=False
                    match_open=False
                    current_match["finished"]=1
    
                    # Add Player 1 to new players data frame if Player 1 not in 
                    # database
    
                    if 'player_ids' in kwargs:
                        if ((current_match["p1"]["id"] \
                            not in kwargs['player_ids']) \
                            and (current_match["p1"]["id"] \
                            not in df_players_new.index.unique()) \
                                 and current_match["p1"]["id"]):
                            try:
                                df_p1=download_player(current_match["p1"]["id"])
                                df_players_new=pd.concat([df_players_new, df_p1])
                            except IndexError:
                                current_match["p1"]["id"]=None
    
                    # Add Player 2 to new players data frame if Player 2 not in 
                    # database
    
                    if 'player_ids' in kwargs:
                        if ((current_match["p2"]["id"] \
                            not in kwargs['player_ids']) \
                            and (current_match["p2"]["id"] \
                            not in df_players_new.index.unique()) \
                            and current_match["p2"]["id"]):
                            try:
                                df_p2=download_player(current_match["p2"]["id"])
                                df_players_new=pd.concat([df_players_new, df_p2])
                            except IndexError:
                                current_match["p2"]["id"]=None
    
                    # Create data frame with new match if match not in old matches
                    # data frame and append to new matches data frame, growing it
                    # by 1
    
                    df_currentmatch=pd.DataFrame({
                            'MatchID':current_match["id_te"],
                            'DateTime':current_match["datetime"],
                            'Tourney':current_tourney_id_composed,
                            'Player1':current_match["p1"]["id"],
                            'Player2':current_match["p2"]["id"],
                            'SetsPlayer1':current_match["score_sets"][0],
                            'SetsPlayer2':current_match["score_sets"][1],
                            'Set1Player1':current_match["scores_p1"][0],
                            'Set2Player1':current_match["scores_p1"][1],
                            'Set3Player1':current_match["scores_p1"][2],
                            'Set4Player1':current_match["scores_p1"][3],
                            'Set5Player1':current_match["scores_p1"][4],
                            'Set1Player2':current_match["scores_p2"][0],
                            'Set2Player2':current_match["scores_p2"][1],
                            'Set3Player2':current_match["scores_p2"][2],
                            'Set4Player2':current_match["scores_p2"][3],
                            'Set5Player2':current_match["scores_p2"][4],
                            'finished':current_match["finished"]},
                                                     index=['MatchID'])
                    df_results_new=pd.concat([df_results_new,df_currentmatch])
                    
                    # Reset current_match dictionary
                    
                    current_match={}
                    current_match["score_sets"]=[]
                    current_match["scores_p1"]=[]
                    current_match["scores_p2"]=[]
                    
            except ValueError:
                match_open=False
                first_player_open=False
                second_player_open=False
                current_match={}
                current_match["score_sets"]=[]
                current_match["scores_p1"]=[]
                current_match["scores_p2"]=[]
                
        
    # Set index of new data frames
    
    df_results_new=df_results_new.set_index("MatchID")

    # Return different set of data frames depending passed kwargs

    if (('player_ids' in kwargs) and ('tourney_ids' not in kwargs)):
        return df_results_new, df_players_new
    
    if (('tourney_ids' in kwargs) and ('player_ids' not in kwargs)):
        return df_results_new, df_tourneys_new
    
    if (('player_ids' in kwargs) and ('tourney_ids' in kwargs)):
        return df_results_new, df_players_new, df_tourneys_new

    return df_results_new

## Downloads current (unfinished) matches for range of dates
## returns pandas dataframe with matches
## start_date: datetime.datetime object containing first date in date range
## end_date: datetime.datetime object containing last date in date range
## matches_type: "atp-single" or "wta-single"
## **kwargs (match_ids, player_ids, tourney_ids): ID lists for matches, 
## players and tourneys in the database  

def download_current_matches (start_date, end_date, matches_type, **kwargs):

    columns_matches=['MatchID',
                     'DateTime',
                     'Tourney',
                     'Player1',
                     'Player2']
    df_matches_new=pd.DataFrame(columns=columns_matches)
    
    # Create list of all dates between start_date and end_date
    
    date_list = [start_date + datetime.timedelta(days=x)
                 for x in range(0, (end_date-start_date).days+1)]

    # Create empty data frames for new results, players, tourneys
    
    if 'player_ids' in kwargs:
        columns_players=['PlayerID',
                         'Name',
                         'Country',
                         'Birthdate',
                         'Gender',
                         'Handed',
                         'Height',
                         'Weight']
        df_players_new=pd.DataFrame(columns=columns_players)
        df_players_new=df_players_new.set_index(['PlayerID'])

    if 'tourney_ids' in kwargs:
        columns_tourneys=['TourneyIDComposed',
                          'TourneyName',
                          'Gender',
                          'Country',
                          'Year',
                          'Surface']
        df_tourneys_new=pd.DataFrame(columns=columns_tourneys)
        df_tourneys_new=df_tourneys_new.set_index(['TourneyIDComposed'])
    
    # Iterate through date list

    for currentdate in date_list:
    
        # Create URL, open TE page, create BS object with page contents
        
        url="http://www.tennisexplorer.com/next/?type=" + \
        matches_type + \
        "&year=" + str(currentdate.year) + \
        "&month=" + str(currentdate.month) + \
        "&day="+str(currentdate.day)
        urlcontents = requests.get(url).text
        soup = BeautifulSoup(urlcontents, "lxml")
        
        # Create empty dictionaries/lists for match/tourney details
        
        current_tourney={}
        current_match={}
        
        # identify <content> tag containing results table for date_list
        
        content_tag_found=False      
        current_content_tag=soup.find("div", {"class":"content"})
        
        while not content_tag_found:
            if _is_currentmatches_table(current_content_tag, currentdate):
                content_tag_found=True
            else:
                current_content_tag=current_content_tag.find_next(
                        "div", {"class":"content"})
        
        # identify <table> tag with results within relevant <content> tag
        # and all <td> tags with single match results
        
        resultsTable = current_content_tag.find("table", {"class":"result"})
        results_tags = resultsTable.find_all("td")
 
        # Define variables to open/close match, Player 1/2 scores
        # These variables delineate between single matches/players
    
        match_open=False
        first_player_open=False
        second_player_open=False
 
        # Iterate through tags in results table
    
        for tag in results_tags:
            
            # Check if tag contains tourney details and fill current_tourney
            # else branch catches tourneys without hyperlink (<a> tag, e.g. 
            # Futures events)
            
            if _is_tourney(tag):
                if tag.find("a"):
                    current_tourney["url"]=list(tag.descendants)[0]["href"]
                    tid=current_tourney["url"][1:]
                    current_tourney["id"]= tid[:tid.index("/")]                                                                          
                    current_tourney["name"]=list(tag.descendants)[-1]
                else:
                    current_tourney["url"]=None
                    current_tourney["name"]=list(tag.descendants)[-1]
                    current_tourney["id"]=current_tourney["name"].replace(" ","-").lower()
                
                
                current_tourney_id_composed=current_tourney["id"] \
                + "-" + matches_type
                currentyear=currentdate.year
                
                # Check if tourney_id exists in database, add to new
                # tourney data frame if missing
                
                if 'tourney_ids' in kwargs:
                    if ((current_tourney_id_composed \
                        not in kwargs['tourney_ids']) \
                        and (current_tourney_id_composed \
                        not in df_tourneys_new.index.unique())):
                        df_t=download_tourney(current_tourney["id"],
                                              matches_type,
                                              currentyear)
                        df_tourneys_new=pd.concat([df_tourneys_new, df_t])
            
            # Check if tag contains match time
            
            if _is_match_time(tag):
    
                # Open match and Player 1 with match time tag
                
                match_open=True
                first_player_open=True
                
                # Fill current_match dictionary with current tourney and
                # date/time (23:59 if time is missing)

                current_match["tourney"]=current_tourney
                try:
                    current_match["datetime"]=str(currentdate.year)+"-"\
                                              +str(currentdate.month)+"-"\
                                              +str(currentdate.day)+" "\
                                              +list(tag.descendants)[0][:2]+":"\
                                              +list(tag.descendants)[0][-2:]+":"\
                                              +"0"
                    datetime.datetime.strptime(current_match["datetime"], 
                                               '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    current_match["datetime"]=str(currentdate.year)+"-"\
                                              +str(currentdate.month)+"-"\
                                              +str(currentdate.day)+" "\
                                              +"23:59:00"
            
            # Extract match details URL and match ID
            
            if match_open and _is_link_matchdetails(tag):
                current_match["url"]=list(tag.descendants)[0]["href"]
                current_match["id_te"]=list(tag.descendants)[0]["href"][18:]
            
            if match_open and _is_player(tag):
                
                # Extract Player 1 details
                
                if first_player_open:
                    try:
                        current_match["p1"]={
                            "name":list(tag.descendants)[1],
                            "url":list(tag.descendants)[0]["href"],
                            "id":list(tag.descendants)[0]["href"][8:-1]}
                    except IndexError:
                        current_match["p1"]={
                            "name":list(tag.descendants)[0],
                            "url":None,
                            "id":None}
                    first_player_open=False
                    second_player_open=True       
                
                # Extract Player 2 details
                
                elif second_player_open:
                    try:
                        current_match["p2"]={
                            "name":list(tag.descendants)[1],
                            "url":list(tag.descendants)[0]["href"],
                            "id":list(tag.descendants)[0]["href"][8:-1]}
                    except IndexError:
                        current_match["p2"]={
                            "name":list(tag.descendants)[0],
                            "url":None,
                            "id":None}
                        
                    # Create data frame with new match if match not in old matches
                    # data frame and append to new matches data frame, growing it
                    # by 1
                                 
                    df_currentmatch=pd.DataFrame({
                            'MatchID':current_match["id_te"],
                            'DateTime':current_match["datetime"],
                            'Tourney':current_tourney_id_composed,
                            'Player1':current_match["p1"]["id"],
                            'Player2':current_match["p2"]["id"]},
                        index=['MatchID'])
                    
                    # Create data frame with new match if match not in old matches
                    # data frame and append to new matches data frame, growing it
                    # by 1
            
                    df_matches_new=pd.concat([df_matches_new,df_currentmatch])
                    second_player_open=False
                    match_open=False   
                            
                    # Add Player 1 to new players data frame if Player 1 not in 
                    # database

                    if 'player_ids' in kwargs:
                        if ((current_match["p1"]["id"] \
                            not in kwargs['player_ids']) \
                            and (current_match["p1"]["id"] \
                            not in df_players_new.index.unique()) \
                                 and current_match["p1"]["id"]):
                            try:
                                df_p1=download_player(current_match["p1"]["id"])
                                df_players_new=pd.concat([df_players_new, df_p1])
                            except IndexError:
                                current_match["p1"]["id"]=None


                    # Add Player 2 to new players data frame if Player 2 not in 
                    # database
        
                    if 'player_ids' in kwargs:
                        if ((current_match["p2"]["id"] \
                            not in kwargs['player_ids']) \
                            and (current_match["p2"]["id"] \
                            not in df_players_new.index.unique()) \
                            and current_match["p2"]["id"]):
                            try:
                                df_p2=download_player(current_match["p2"]["id"])
                                df_players_new=pd.concat([df_players_new, df_p2])
                            except IndexError:
                                current_match["p2"]["id"]=None
            
                    # Reset current_match dictionary
                    
                    current_match={}
                    current_match["score_sets"]=[]
                    current_match["scores_p1"]=[]
                    current_match["scores_p2"]=[]
                    
    df_matches_new=df_matches_new.set_index(['MatchID'])
    
    # Return different set of data frames depending passed kwargs

    if (('player_ids' in kwargs) and ('tourney_ids' not in kwargs)):
        return df_matches_new, df_players_new
    
    if (('tourney_ids' in kwargs) and ('player_ids' not in kwargs)):
        return df_matches_new, df_tourneys_new
    
    if (('player_ids' in kwargs) and ('tourney_ids' in kwargs)):
        return df_matches_new, df_players_new, df_tourneys_new

    return df_matches_new

## Downloads odds for a given list of match IDs
## Input: list of match IDs
## Output: Dataframe containing all available odds on TennisExplorer    

def download_odds(matches_list):
    
    # initialize output data frame and timestamp
    odds_columns=['MatchID',
                  'Bookie',
                  'Timestamp',
                  'Type',
                  'Value',
                  'Odds1',
                  'Odds2',
                  'OddsIDComposed']
    df_odds=pd.DataFrame(columns=odds_columns)
    timestamp=datetime.datetime.now()
    
    # iterate through match IDs in matches_list    
    for match in matches_list:
    
        # open match page on TE and create BS object
        odds_url="https://www.tennisexplorer.com/match-detail/?id="+str(match)
        urlcontents = requests.get(odds_url).text
        odds_soup = BeautifulSoup(urlcontents, "lxml")
        odds_counter=0
        
        current_odds_type="home-away"
        # find html content containing home/away odds
        try:
            odds_tags=odds_soup.find("div", {'id':['oddsMenu-1-data']}).find(
                "tbody").find_all()
        except AttributeError:
            odds_tags=[]
        if len(odds_tags)>0:
            current_odds={}
            bets_open=True           
            # iterate through odds tags and read odds into dictionary
            for tag in odds_tags:
                for inner_tag in tag:
                    if bets_open and _is_bookie(inner_tag):
                        current_bookie=list(inner_tag.descendants)[-1]
                    if bets_open and _is_odds_home(inner_tag):
                        current_odds['odds1']=float(list(inner_tag.descendants)[1])
                    if bets_open and _is_odds_away(inner_tag):
                        current_odds['odds2']=float(list(inner_tag.descendants)[1])
                        # convert odds dictionary to data frame and concatenate
                        # with df_odds
                        df_currentodds=pd.DataFrame({
                                'MatchID':match,
                                'Bookie':current_bookie,
                                'Timestamp':timestamp,
                                'Type':current_odds_type,
                                'Value':1.0,
                                'Odds1':current_odds['odds1'],
                                'Odds2':current_odds['odds2'],
                                'OddsIDComposed':str(match) \
                                + "-"+current_bookie.lower().replace(" ","-") \
                                + "-"+current_odds_type \
                                + "-"+timestamp.strftime("%Y%m%d-%H%M%S")
                                },index=['OddsIDComposed'])
                        df_odds=pd.concat([df_odds,df_currentodds])
                        odds_counter+=1
                        current_odds={}
                    # use average odds tag as closing tag for home/away odds
                    if _is_average_odds(inner_tag):
                        bets_open=False
                        
        # find html content containing over/under odds            
        try:
            odds_tags=odds_soup.find("div", {'id':['oddsMenu-2-data']}).find(
                "tbody").find_all()
        except AttributeError:
            odds_tags=[]
        if len(odds_tags)>0:
            current_odds={}
            bets_open=True
            # iterate through odds tags and read odds into dictionary
            for tag in odds_tags:
                for inner_tag in tag:
                    if _is_bookie(inner_tag):
                        current_bookie=list(inner_tag.descendants)[-1]
                        bets_open=True
                    if _is_odds_type(inner_tag):
                        current_odds_type="over-under-"+list(
                                inner_tag.descendants)[0][-5:].replace(
                                        " ","")
                    if bets_open and _is_odds_value(inner_tag):
                        try:
                            current_odds['value']=float(list(inner_tag.descendants)[0])
                        except ValueError:
                            current_odds['value']=None
                    if bets_open and _is_odds_home(inner_tag):
                        current_odds['odds1']=float(list(inner_tag.descendants)[1])
                    if bets_open and _is_odds_away(inner_tag):
                        current_odds['odds2']=float(list(inner_tag.descendants)[1])
                        # convert odds dictionary to data frame and concatenate
                        # with df_odds
                        df_currentodds=pd.DataFrame({
                                'MatchID':match,
                                'Bookie':current_bookie,
                                'Timestamp':timestamp,
                                'Type':current_odds_type,
                                'Value':current_odds['value'],
                                'Odds1':current_odds['odds1'],
                                'Odds2':current_odds['odds2'],
                                'OddsIDComposed':str(match) \
                                + "-"+current_bookie.lower().replace(" ","-") \
                                + "-"+current_odds_type \
                                + "-"+str(current_odds['value'])\
                                + "-"+timestamp.strftime("%Y%m%d-%H%M%S")
                                },index=['OddsIDComposed'])
                        df_odds=pd.concat([df_odds,df_currentodds])
                        odds_counter+=1
                        current_odds={}
                    # use average odds tag as closing tag for over/under odds
                    if _is_average_odds(inner_tag):
                        bets_open=False
        
        # find html content containing Asian handicap odds             
        try:
            odds_tags=odds_soup.find("div", {'id':['oddsMenu-3-data']}).find(
                "tbody").find_all()
        except AttributeError:
            odds_tags=[]
        if len(odds_tags)>0:
            current_odds={}
            bets_open=True
            # iterate through odds tags and read odds into dictionary
            for tag in odds_tags:
                for inner_tag in tag:
                    if _is_bookie(inner_tag):
                        current_bookie=list(inner_tag.descendants)[-1]
                        bets_open=True
                    if _is_odds_type(inner_tag):
                        if list(inner_tag.descendants)[0][-3:]=="set":
                            extension="sets"
                        elif list(inner_tag.descendants)[0][-4:]=="sets":
                            extension="sets"
                        elif list(inner_tag.descendants)[0][-5:]=="games":
                            extension="games"
                        elif list(inner_tag.descendants)[0][-4:]=="game":
                            extension="games"
                        current_odds_type="asian-handicap-"+extension
                    if bets_open and _is_odds_value(inner_tag):
                        try:
                            current_odds['value']=float(list(inner_tag.descendants)[0])
                        except ValueError:
                            current_odds['value']=None 
                    if bets_open and _is_odds_home(inner_tag):
                        current_odds['odds1']=float(list(inner_tag.descendants)[1])
                    if bets_open and _is_odds_away(inner_tag):
                        current_odds['odds2']=float(list(inner_tag.descendants)[1])
                        # convert odds dictionary to data frame and concatenate
                        # with df_odds
                        df_currentodds=pd.DataFrame({
                                'MatchID':match,
                                'Bookie':current_bookie,
                                'Timestamp':timestamp,
                                'Type':current_odds_type,
                                'Value':current_odds['value'],
                                'Odds1':current_odds['odds1'],
                                'Odds2':current_odds['odds2'],
                                'OddsIDComposed':str(match) \
                                + "-"+current_bookie.lower().replace(" ","-") \
                                + "-"+current_odds_type \
                                + "-"+str(current_odds['value'])\
                                + "-"+timestamp.strftime("%Y%m%d-%H%M%S")
                                },index=['OddsIDComposed'])
                        df_odds=pd.concat([df_odds,df_currentodds])
                        odds_counter+=1
                        current_odds={}
                    # use average odds tag as closing tag for over/under odds
                    if _is_average_odds(inner_tag):
                        bets_open=False      
        
        # find html content containing exact score odds  
        current_odds_type="correct-score"
        try:
            odds_tags=odds_soup.find("div", {'id':['oddsMenu-4-data']}).find(
                "tbody").find_all()
        except AttributeError:
            odds_tags=[]
        if len(odds_tags)>0:
            current_odds={}
            bets_open=True
            # iterate through odds tags and read odds into dictionary
            for tag in odds_tags:
                for inner_tag in tag:
                    if _is_bookie(inner_tag):
                        current_bookie=list(inner_tag.descendants)[-1]
                        bets_open=True
                    if bets_open and _is_odds_value(inner_tag):
                        try:
                            current_odds['value']=int(list(inner_tag.descendants)[0][0]) \
                            - int(list(inner_tag.descendants)[0][-1])
                        except ValueError:
                            current_odds['value']=None 
                    if bets_open and _is_odds_home(inner_tag):
                        current_odds['odds1']=float(list(inner_tag.descendants)[1])
                        # convert odds dictionary to data frame and concatenate
                        # with df_odds
                        df_currentodds=pd.DataFrame({
                                'MatchID':match,
                                'Bookie':current_bookie,
                                'Timestamp':timestamp,
                                'Type':current_odds_type,
                                'Value':current_odds['value'],
                                'Odds1':current_odds['odds1'],
                                'Odds2':None,
                                'OddsIDComposed':str(match) \
                                + "-"+current_bookie.lower().replace(" ","-") \
                                + "-"+current_odds_type \
                                + "-"+str(current_odds['value'])\
                                + "-"+timestamp.strftime("%Y%m%d-%H%M%S")
                                },index=['OddsIDComposed'])
                        df_odds=pd.concat([df_odds,df_currentodds])
                        odds_counter+=1
                        current_odds={}
                    # use average odds tag as closing tag for over/under odds
                    if _is_average_odds(inner_tag):
                        bets_open=False
        
#        if odds_counter==0:
#            print("No odds for match "+str(match)+" found")
#        else:                    
#            print(str(odds_counter)+" odds for match " \
#                  + str(match)+" added")
    
    df_odds=df_odds.set_index(['OddsIDComposed'])
    return df_odds

# Calculate new Elo ratings from old Elo ratings, match winner and factor
# (factor being 25, 50 or 100)

def calculate_elo(elo1,elo2,winner,factor):
    elo1_delta = (-winner+2-(1/(1+10**((elo2-elo1)/400))))*factor
    elo2_delta = (winner-1-(1/(1+10**((elo1-elo2)/400))))*factor
    return elo1+elo1_delta, elo2+elo2_delta