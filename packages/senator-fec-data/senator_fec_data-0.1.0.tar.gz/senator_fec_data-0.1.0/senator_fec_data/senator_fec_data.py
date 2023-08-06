from bs4 import BeautifulSoup
import os
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from xml.etree.ElementTree import parse

def get_api_key(api_key):
    """
    Returns a key for convenient use in package functions.
    
    Parameters:
    ------------
    api_key: str.
    The name of an FEC API key saved in the user's operating system.
    
    Output:
    ------------
    key: str.
    A variable "key" that can be saved for future use.
    
    Example:
    ------------
    >> key = get_api_key("FEC_API_KEY")
    >> print(type(key))
    <class 'str'>
    """
    key = os.getenv(api_key)
    return key

def get_senator_list():
    """
    Returns a pandas DataFrame of current U.S. Senators.
    
    Parameters:
    ------------
    
    Output:
    ------------
    A pandas DataFrame object with three columns: first_name, last_name, and state.
    
    Example:
    ------------
    >> senator_list = get_senator_list()
    >> type(senator_list)
    pandas.core.frame.DataFrame
    """
    document = parse('senator_fec_data/data/senators_cfm.xml')

    first_name = []
    last_name = []
    state = []

    for item in document.iterfind('member'):
        first_name.append(item.findtext('first_name'))
        last_name.append(item.findtext('last_name'))
        state.append(item.findtext('state'))
    
    senator_list = pd.DataFrame({'first_name': first_name, 'last_name': last_name, 'state':state})
    senator_list["full_name"] = senator_list["first_name"] + " " + senator_list["last_name"]
    
    return senator_list

def get_senator(state):    
    """
    Returns the two senators from a specified U.S. state.
    
    Parameters:
    ------------
    state: str.
    A string abbreviation of one of the 50 U.S. states.
    
    Output:
    ------------
    senators: obj.
    The full names of the U.S. senators for the specified state.
    
    Example:
    ------------
    >> get_senator("MA")
    57    Edward J. Markey
    95    Elizabeth Warren
    Name: full_name, dtype: object
    """
    assert isinstance(state, str), "This function only works with state names as strings."
    senator_list = get_senator_list()
    senators = senator_list[senator_list["state"] == state]
    senators = senators["full_name"]
    if senators.empty == True:
        print("This input is not supported. Try an abbreviation of one of the 50 states.")
    else:
        return senators
    
def get_senator_id(senator, key):
    """
    Returns the FEC campaign ID from the senator's Senate campaigns. This ID will be the same for every time he or she
    runs for the Senate, but will not include House or Presidency campaigns.
    
    Parameters:
    ------------
    senator: str.
    The full name of a sitting U.S. senator. The use of a nickname will result in error.
    key: str.
    The user's FEC API key, saved from the function get_api_key().
    
    Output:
    ------------
    df_id_return: str.
    The FEC ID of a sitting U.S. senator.
    
    Example:
    ------------
    >> get_senator_id("Elizabeth Warren")
    'S2MA00170'
    """
    assert isinstance(senator, str), "This function only works with senator names as strings."
    try:
        candidate_call = "https://api.open.fec.gov/v1/names/candidates/?api_key=" + key + "&q=" + senator
        candidate_id_call = requests.get(candidate_call)
        json_candidate_id = candidate_id_call.json()
        df_id = pd.DataFrame(json_candidate_id['results'])
        df_id = df_id[df_id["office_sought"] == "S"]
        df_id_return = str(df_id["id"].iloc[0])
        return df_id_return
    except (KeyError):
        print("This senator could not be found. Please try the name of a current U.S. senator.")
        
def get_state_ids(state, key):
    """
    Returns the FEC campaign ID from both state senators. This ID will be the same for every time the candidate 
    runs for the Senate, but will not include House or Presidency campaigns.
    
    Parameters:
    ------------
    state: str.
    The abbreviation of one of 50 U.S. states.
    key: str.
    The user's FEC API key, saved from the function get_api_key().
    
    Output:
    ------------
    df_id_return: str.
    The FEC ID of a sitting U.S. senator. The output will produce two strings.
    
    Example:
    ------------
    >> get_state_ids("MA")
    S4MA00028
    S2MA00170
    """
    assert isinstance(state, str), "This function only works with state names as strings."
    try:
        for senator in get_senator(state):
            print(get_senator_id(senator, key))
    except TypeError as e:
        print(f"An error has occurred: {e}. Please check your inputs.")

        
def get_fec_totals_senator(senator, key):
    """
    Returns a pandas DataFrame to the user with the specified U.S. senator's full FEC filings.
    
    Parameters:
    ------------
    senator: str.
    The full name of a sitting U.S. senator.
    key: str.
    The user's FEC API key, saved from the function get_api_key().
    
    Output:
    ------------
    df_sched_e: pandas DataFrame.
    Pandas DataFrame with full FEC information for the senator. Will be stored in the user's folder.
    
    Example:
    ------------
    >> get_fec_totals_senator("Elizabeth Warren")
    """
    assert isinstance(senator, str), "This function only works with senator names as strings."
    key = os.getenv("FEC_API_KEY")
    try:
        senator_id = get_senator_id(senator, key)
        schedule_e_call = "https://api.open.fec.gov/v1/candidate/" + senator_id + "/totals/?api_key=" + key  
        call_expenditures = requests.get(schedule_e_call)
    
        json_sched_e = call_expenditures.json()
        df_sched_e = pd.DataFrame(json_sched_e['results'])
        df_sched_e = df_sched_e.sort_values(by=['last_report_year'])
        df_sched_e = df_sched_e.drop_duplicates(subset = 'last_report_year')
        df_sched_e.to_csv(f"{senator} FEC Data", index= True)
        print("Success! Check your folder for the dataset.")
    except (TypeError, KeyError) as e:
        print(f"{senator} could not be found. Please try the full name of a current U.S. senator. Error:{e}")
        
 

def get_fec_totals_state(state, key):
    """
    Returns a pandas DataFrame to the user with the specified U.S. senator's full FEC filings.
    
    Parameters:
    ------------
    state: str.
    An abbreviation of one of the 50 U.S. states.
    key: str.
    The user's FEC API key, saved from the function get_api_key().
    
    Output:
    ------------
    df_sched_e: pandas DataFrame.
    Pandas DataFrame with full FEC information for the senator. Will be stored in the user's folder. One
    file will appear for each state senator.
    
    Example:
    ------------
    >> get_fec_totals_senator("NY")
    """
    assert isinstance(state, str), "This function only works with state names as strings."
    try:
        for senator in get_senator(state):
            get_fec_totals_senator(senator, key)
    except TypeError as e:
        print(f"An error has occurred: {e}. Please check your inputs.")
        
        

def lifetime_contributions_senator(senator, key):
    """
    Returns the lifetime FEC unitemized contributions for the specified senator.
    
    Parameters:
    ------------
    senator: str.
    The full name of a sitting U.S. senator.
    key: str.
    The user's FEC API key, saved from the function get_api_key().
    
    Output:
    ------------
    str.
    Total lifetime unitemized contributions for the senator.
    
    Example:
    ------------
    >> lifetime_contributions_senator("Elizabeth Warren")
    Elizabeth Warren has raised a total of $47963846.95 in unitemized contributions in his or her life.
    """
    key = os.getenv("FEC_API_KEY")
    assert isinstance(senator, str), "This function only works with senator names as strings."
    try:
        senate_candidate_id = get_senator_id(senator, key)
        schedule_e_call = "https://api.open.fec.gov/v1/candidate/" + senate_candidate_id + "/totals/?api_key=" + key  
        call_expenditures = requests.get(schedule_e_call)
    
        json_sched_e = call_expenditures.json()
        df_sched_e = pd.DataFrame(json_sched_e['results'])
        df_sched_e = df_sched_e.sort_values(by=['last_report_year'])
        df_sched_e = df_sched_e.drop_duplicates(subset = 'last_report_year')
        lifetime_contributions = df_sched_e["individual_unitemized_contributions"].sum()
        print(f'{senator} has raised a total of ${lifetime_contributions} in unitemized contributions in his or her life.')
    except NameError as e:
        print(f"An error has occurred: {e}. Please check your inputs.")
        
        
def lifetime_contributions_state(state, key):
    """
    Returns the lifetime FEC unitemized contributions for both state senators.
    
    Parameters:
    ------------
    state: str.
    An abbreviation of one of 50 U.S. states.
    key: str.
    The user's FEC API key, saved from the function get_api_key().
    
    Output:
    ------------
    str.
    Total lifetime unitemized contributions for both state senators.
    
    Example:
    ------------
    >> lifetime_contributions_state("MA")
    Edward J. Markey has raised a total of $6853866.85 in unitemized contributions in his or her life.
    Elizabeth Warren has raised a total of $47963846.95 in unitemized contributions in his or her life.
    """
    assert isinstance(state, str), "This function only works with state names as strings."
    try:
        for senator in get_senator(state):
            lifetime_contributions_senator(senator, key)
    except TypeError as e:
        print(f"An error has occurred: {e}. Please check your inputs.")
        
        
        
def lifetime_expenditures_senator(senator, key):
    """
    Returns the lifetime FEC expenditures for the specified senator.
    
    Parameters:
    ------------
    senator: str.
    The full name of a sitting U.S. senator.
    key: str.
    The user's FEC API key, saved from the function get_api_key().
    
    Output:
    ------------
    str.
    Total lifetime expenditures contributions for the specified senator.
    
    Example:
    ------------
    >> lifetime_contributions_state("Elizabeth Warren")
    Elizabeth Warren has spent a total of $69572641.42999999 through his or her campaigns for the Senate.
    """
    key = os.getenv("FEC_API_KEY")
    assert isinstance(senator, str), "This function only works with senator names as strings."
    try:
        senate_candidate_id = get_senator_id(senator, key)
    
        schedule_e_call = "https://api.open.fec.gov/v1/candidate/" + senate_candidate_id + "/totals/?api_key=" + key  
        call_expenditures = requests.get(schedule_e_call)
    
        json_sched_e = call_expenditures.json()
        df_sched_e = pd.DataFrame(json_sched_e['results'])
        df_sched_e = df_sched_e.sort_values(by=['last_report_year'])
        df_sched_e = df_sched_e.drop_duplicates(subset = 'last_report_year')
        lifetime_contributions = df_sched_e["operating_expenditures"].sum()
        print(f'{senator} has spent a total of ${lifetime_contributions} through his or her campaigns for the Senate.')
    except NameError as e:
        print(f"An error has occurred: {e}. Please check your inputs.")
    except NameError as e:
        print(f"An error has occurred: {e}. Please check your inputs.")
        
        
        
def lifetime_expenditures_state(state, key):
    """
    Returns the lifetime FEC expenditures for both state senators.
    
    Parameters:
    ------------
    state: str.
    An abbreviation of one of 50 U.S. states.
    key: str.
    The user's FEC API key, saved from the function get_api_key().
    
    Output:
    ------------
    str.
    Total lifetime unitemized contributions for both state senators.
    
    Example:
    ------------
    >> lifetime_expenditures_state("MA")
    Edward J. Markey has spent a total of $29908338.22 through his or her campaigns for the Senate.
    Elizabeth Warren has spent a total of $69572641.42999999 through his or her campaigns for the Senate.
    """
    assert isinstance(state, str), "This function only works with state names as strings."
    try:
        for senator in get_senator(state):
            lifetime_expenditures_senator(senator, key)
    except TypeError as e:
        print(f"An error has occurred: {e}. Please check your inputs.")
        
        
def get_fec_expenditures_senator(senator, key):
    """
    Produces a plot of FEC expenditures by year.
    
    Parameters:
    ------------
    senator: str.
    The full name of a sitting U.S. senator.
    key: str.
    The user's FEC API key, saved from the function get_api_key().
    
    Output:
    ------------
    obj.
    A plot of senator expenditures by year.
    
    Example:
    ------------
    >> get_fec_expenditures_senator("Elizabeth Warren")
    <function show at 0x7fe79a2cb5f0>
    """
    key = os.getenv("FEC_API_KEY")
    assert isinstance(senator, str), "This function only works with senator names as strings."
    try:
        senate_candidate_id = get_senator_id(senator, key)
        schedule_e_call = "https://api.open.fec.gov/v1/candidate/" + senate_candidate_id + "/totals/?api_key=" + key  
        call_expenditures = requests.get(schedule_e_call)
    
        json_sched_e = call_expenditures.json()
        df_sched_e = pd.DataFrame(json_sched_e['results'])
        df_sched_e = df_sched_e.sort_values(by=['last_report_year'])
        df_sched_e = df_sched_e.drop_duplicates(subset = 'last_report_year')
        df_sched_e.plot.bar(x = 'last_report_year', y = ['receipts'], rot = 40, legend = None)
        plt.xlabel("Report Year")
        plt.ylabel("Dollars in Millions")
        plt.title(f"Over Time Campaign Expenditures for {senator}")
        print(plt.show)
    except NameError as e:
        print(f"An error has occurred: {e}. Please check your inputs.")
        
        
def get_fec_expenditures_state(state, key):
    """
    Produces plots of FEC expenditures by year.
    
    Parameters:
    ------------
    state: str.
    The abbreviated name of one of 50 U.S. states.
    key: str.
    The user's FEC API key, saved from the function get_api_key().
    
    Output:
    ------------
    obj.
    Two plots of senator expenditures by year.
    
    Example:
    ------------
    >> get_fec_expenditures_state("MA")
    <function show at 0x7fe79a2cb5f0>
    """
    assert isinstance(state, str), "This function only works with state names as strings."
    try:
        for senator in get_senator(state):
            get_fec_expenditures_senator(senator, key)
    except TypeError as e:
        print(f"An error has occurred: {e}. Please check your inputs.")
        
        
def get_fec_contributions_senator(senator, key):
    """
    Produces a plot of FEC unitemized contributions by year.
    
    Parameters:
    ------------
    senator: str.
    The name of a sitting U.S. senator.
    key: str.
    The user's FEC API key, saved from the function get_api_key().
    
    Output:
    ------------
    obj.
    A plot of unitemized contributions by year.
    
    Example:
    ------------
    >> get_fec_contributions_state("Elizabeth Warren")
    <function show at 0x7fe79a2cb5f0>
    """
    key = os.getenv("FEC_API_KEY")
    assert isinstance(senator, str), "This function only works with senator names as strings."
    try:
        senate_candidate_id = get_senator_id(senator, key)
        schedule_e_call = "https://api.open.fec.gov/v1/candidate/" + senate_candidate_id + "/totals/?api_key=" + key  
        call_expenditures = requests.get(schedule_e_call)
    
        json_sched_e = call_expenditures.json()
        df_sched_e = pd.DataFrame(json_sched_e['results'])
        df_sched_e = df_sched_e.sort_values(by=['last_report_year'])
        df_sched_e = df_sched_e.drop_duplicates(subset = 'last_report_year')
        df_sched_e.plot.bar(x = 'last_report_year', y = ['individual_unitemized_contributions'], rot = 40, legend = None)
        plt.xlabel("Report Year")
        plt.ylabel("Dollars in Millions")
        plt.title(f"Over Time Individual Unitemized Contributions for {senator}")
        print(plt.show)
    except NameError as e:
        print(f"An error has occurred: {e}. Please check your inputs.")
        
        
def get_fec_contributions_state(state, key):
    """
    Produces plots of FEC unitemized contributions by year.
    
    Parameters:
    ------------
    state: str.
    The abbreviated name of one of 50 U.S. states.
    key: str.
    The user's FEC API key, saved from the function get_api_key().
    
    Output:
    ------------
    obj.
    Two plots of senator contributions by year.
    
    Example:
    ------------
    >> get_fec_contributions_state("MA")
    <function show at 0x7fe79a2cb5f0>
    <function show at 0x7fe79a2cb5f0>
    """
    assert isinstance(state, str), "This function only works with state names as strings."
    try:
        for senator in get_senator(state):
            get_fec_contributions_senator(senator, key)
    except TypeError as e:
        print(f"An error has occurred: {e}. Please check your inputs.")
        
        
        
def full_report_senator(senator, key):
    """
    Produces a full report and visualizations of the U.S. senator's FEC data.
    
    Parameters:
    ------------
    senator: str.
    The full name of a sitting U.S. senator.
    key: str.
    The user's FEC API key, saved from the function get_api_key().
    
    Output:
    ------------
    str.: The lifetime unitemized contributions of the senator.
    str.: The lifetime expenditures of the senator.
    obj.: A plot of senator expenditures by year.
    obj.: A plot of senator unitemized contributions by year.
    
    Example:
    ------------
    >> full_report_senator("Elizabeth Warren")
    Report on Elizabeth Warren:
    ---------------------------
    Elizabeth Warren has raised a total of $47963846.95 in unitemized contributions in his or her life.
    Elizabeth Warren has spent a total of $69572641.42999999 through his or her campaigns for the Senate.
    <function show at 0x7fe79a2cb5f0>
    <function show at 0x7fe79a2cb5f0>
    """
    assert isinstance(senator, str), "This function only works with senator names as strings."
    try:
        print(f"Report on {senator}:")
        print("---------------------------")
        lifetime_contributions_senator(senator, key)
        lifetime_expenditures_senator(senator, key)
    
        get_fec_expenditures_senator(senator, key)
        get_fec_contributions_senator(senator, key)
    except IndexError as e:
        print(f"An error has occurred: {e}. Please check your inputs.")