import fastf1 as ff1
import pandas as pd
import numpy as np

## Extract Details
def mnl_identify_conventional_events(yr):
    event_schedule = ff1.get_event_schedule(yr)
    conventional_events = event_schedule[event_schedule['EventFormat']=='conventional'].reset_index().drop('index', axis=1)
    return conventional_events

def mnl_extract_session(yr, event_num, conventional_events, session_type):
    rn = conventional_events.iloc[event_num]['RoundNumber']
    try:
      session = ff1.get_session(yr,rn,session_type)
      session.load()
      df = session.laps
      #Weather Data
      df_weather = session.weather_data
      
      return df, df_weather
    except:
      error_msg = f"Cannot pull {session_type} from FastF1, will skip the whole session"
      error = True
      return error, error_msg     

def mnl_extract_event_data(yr, event_num, conventional_events):
    #Base Information
    round_number = conventional_events.iloc[event_num]['RoundNumber']
    championship_progress = round_number /conventional_events['RoundNumber'].max()
    temp_event = ff1.get_event(yr,round_number)
    circuit = temp_event.Location
    
    base_info = {
        'round_number': round_number,
        'championship_progress': championship_progress,
        'circuit': circuit
    }
    
    #Extract Events
    df_fp1,weather_fp1 = mnl_extract_session(yr, event_num, conventional_events, 'FP1')
    df_fp2,weather_fp2 = mnl_extract_session(yr, event_num, conventional_events, 'FP2')
    df_fp3,weather_fp3 = mnl_extract_session(yr, event_num, conventional_events, 'FP3')
    df_qual,weather_qual = mnl_extract_session(yr, event_num, conventional_events, 'Q')

    return base_info, df_fp1, df_fp2, df_fp3, df_qual, weather_fp1, weather_fp2, weather_fp3, weather_qual