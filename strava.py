import requests
import time
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import matplotlib.pyplot as plt
import urllib3
import os

def get_access_token() -> str:
    urllib3.disable_warnings()

    client_id:int=os.environ.get("CLIENT_ID")
    client_secret:str=os.environ.get("CLIENT_SECRET")
    refresh_token:str=os.environ.get("REFRESH_TOKEN")

    auth_endpoint:str = "https://www.strava.com/oauth/token"
    payload:dict = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': "refresh_token"
        }
    
    res = requests.post(auth_endpoint, data=payload, verify=False)
    return res.json()['access_token']


def get_strava_df(access_token:str) -> pd.pandas.core.frame.DataFrame:
    urllib3.disable_warnings()
    activites_endpoint:str = "https://www.strava.com/api/v3/athlete/activities"

    #ile aktywności wyciągamy za jednym zapytaniem
    per_page = 50

    # create time window, strava accepts time in epoch format
    before = int(time.time())
    after = int(time.mktime( (dt.datetime.now() - relativedelta(years=1)).timetuple() ))
    # print(f'Timeframe: before: {before} -> {time.strftime("%Y-%m-%d %H:%M", time.localtime(before))}, after: {after} -> {time.strftime("%Y-%m-%d %H:%M", time.localtime(after))}')

    headers:dict = {'Authorization': f'Authorization: Bearer {access_token}'}
    payload:dict = {
        'before': before, # An epoch timestamp to use for filtering activities that have taken place before a certain time.
        'after' : after, # An epoch timestamp to use for filtering activities that have taken place after a certain time.
        'page'  : 1,
        'per_page': per_page
    }

    #wyciągamy po per_page aktywności za jednym razem
    #iterujemy pętlę, tak długo aż nie będzię nowych aktywności

    activites = []
    while True:
        r = requests.get(activites_endpoint, params=payload, headers=headers, verify=False)
        # print(f"Status code: {r.status_code}")
        a = r.json() #wyciągamy odpowiedź
        if len(a) > 0 and len(a) < per_page: #jeżeli wróciło mniej niż per_page aktywności to znaczy, że więcej nie ma
            activites += r.json()
            # print("There is no more.")
            break
        else:
            activites += r.json()
            payload['page'] +=1
            # print(f'there is more: page={payload["page"]}')
            time.sleep(2)

    # tworzymy dataframe
    df = pd.DataFrame.from_dict(activites)

    #układamy sobie dane :)
    # 1. zmienmy na obiekt datetime: 2023-12-27T12:45:33Z -> %Y-%m-%dT%M:%SZ, ale użyjemy sprytniejszego czegoś :)
    df['start_date_local'] = pd.to_datetime(df['start_date_local'], format='ISO8601')

    return df

def plot_suffer_score(df:pd.pandas.core.frame.DataFrame) -> None:

    #suffer score
    #df[['sport_type', 'suffer_score']].groupby('sport_type').count().plot.bar()
    #df[df['sport_type'].str.match('VirtualRide')]['suffer_score'].plot.box()

    ride  = df[df['sport_type'].str.match('Ride')]['suffer_score'].dropna()
    vride = df[df['sport_type'].str.match('VirtualRide')]['suffer_score'].dropna()
    swim = df[df['sport_type'].str.match('Swim')]['suffer_score'].dropna()

    fig, ax = plt.subplots()
    ax.boxplot([ride, vride, swim])
    ax.set_title('Suffer score')
    plt.xticks([1, 2, 3], ['Ride', 'VRide', 'Swim'])
    plt.show()

def get_flash(df:pd.pandas.core.frame.DataFrame) -> str:
    forecast = {}
    forecast['activities_per_year'] = (52-4)*3 #52 tygodnie - 4 tygodnie wakacyjne -> 144 aktywności
    flash = {}

    flash['current_year'] = dt.datetime.today().year
    flash['days_in_current_year'] = 365 if flash['current_year'] % 4 else 365 #zakładam, że do 2100 roku nie dożyję :)
    flash['number_of_days_passed_this_year'] = (dt.datetime.today() - dt.datetime(flash['current_year'],1,1)).days + 1
    flash['percent_of_days_passed_this_year'] = round(flash['number_of_days_passed_this_year']/flash['days_in_current_year'] * 100,2)
    flash['activities_year_2_date'] = len(df)
    flash['performance_year_2_date'] = flash['activities_year_2_date'] / forecast['activities_per_year']

    return f"Forecast: {forecast['activities_per_year']} activities.\n" + \
        f"Till the end of the year left {flash['days_in_current_year'] - flash['number_of_days_passed_this_year']} days\n" + \
        f"Performance year-to-date: {round(flash['performance_year_2_date'] * 100,2)}% ({flash['activities_year_2_date']} activities)."


if __name__ == "__main__":
    access_token = get_access_token()
    df = get_strava_df(access_token)
    print(get_flash(df))
    # plot_suffer_score(df)