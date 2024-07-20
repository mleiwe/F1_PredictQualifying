import fastf1 as ff1
import pandas as pd
import numpy as np
from FastF1_DataAccess import fastf1_extract
from FastF1_DataAccess import fastf1_transform

## Session Extractions
def mnl_ExtractPracticeSessionData(df, df_weather, driver_nums, df_qual, prefix):
    #Get weather information
    air_temp_mean = df_weather['AirTemp'].mean()
    humidity_mean = df_weather['Humidity'].mean()
    pressure_mean = df_weather['Pressure'].mean()
    rainfall_mean = df_weather['Rainfall'].mean()
    track_temp_mean = df_weather['TrackTemp'].mean()
    wind_speed_mean = df_weather['WindSpeed'].mean()
    
    #Get general session information - i.e. fastest times etc.
    fastest_session_data = fastf1_transform.mnl_get_fastest_session_times(df)
    session_dict = {}
    #Loop per driver
    for driver_num in driver_nums:
        driver_df, df_teammate = fastf1_transform.mnl_get_driver_and_teammate_dataframes(df,driver_num, df_qual)
        driver_name = driver_df[driver_df['DriverNumber']==driver_num].iloc[0]['Driver']
        driver_team = driver_df[driver_df['DriverNumber']==driver_num].iloc[0]['Team']
        driver_session_data = fastf1_transform.mnl_get_driver_session_details(driver_df, df_weather, fastest_session_data, driver_name, driver_num, driver_team)
        teammate_session_data = {}
        if not df_teammate.empty:
            teammate_nums = df_teammate['DriverNumber'].unique()
            for teammate_num in teammate_nums:
                teammate_name = df_teammate[df_teammate['DriverNumber']==teammate_num].iloc[0]['Driver']
                ts = fastf1_transform.mnl_get_driver_session_details(df_teammate, df_weather, fastest_session_data, teammate_name, teammate_num, driver_team)
                teammate_session_data.update(ts)
        else:
            teammate_session_data = fastf1_transform.mnl_generate_empty_driver_session()
        comparison_session_data = fastf1_transform.mnl_compare_drivers(driver_session_data,teammate_session_data)
        driver_all = fastf1_transform.mnl_concat_dictionaries(driver_session_data, teammate_session_data,comparison_session_data)
        driver_session = fastf1_transform.mnl_add_session_prefix(driver_all,prefix)
        #If this is the first driver specify the keys
        if not session_dict:
            keys = driver_session.keys()
            for key in keys:
                session_dict[key]=[] 
            session_dict[prefix + "_" + 'air_temp_mean'] = []
            session_dict[prefix + "_" + 'humidity_mean'] = []
            session_dict[prefix + "_" + 'pressure_mean'] = []
            session_dict[prefix + "_" + 'rainfall_mean'] = []
            session_dict[prefix + "_" + 'track_temp_mean'] = []
            session_dict[prefix + "_" + 'wind_speed_mean'] = []
        session_dict = fastf1_transform.mnl_update_session_dictionary(session_dict,driver_session)
        
        #Add the weather
        session_dict[prefix + "_" + 'air_temp_mean'].append(air_temp_mean)
        session_dict[prefix + "_" + 'humidity_mean'].append(humidity_mean)
        session_dict[prefix + "_" + 'pressure_mean'].append(pressure_mean)
        session_dict[prefix + "_" + 'rainfall_mean'].append(rainfall_mean)
        session_dict[prefix + "_" + 'track_temp_mean'].append(track_temp_mean)
        session_dict[prefix + "_" + 'wind_speed_mean'].append(wind_speed_mean)
    return session_dict

def mnl_ExtractQualifyingData(df, df_weather, driver_nums):
    session_dict = {}
    #Loop per driver
    for driver_num in driver_nums:
        qual_details = fastf1_transform.mnl_get_fastest_qualifying_lap(df, df_weather, driver_num)
        #Update session_dict
        if not session_dict:
            keys = qual_details.keys()
            for key in keys:
                session_dict[key] = []
        keys = qual_details.keys()
        for key in keys:
            session_dict[key].append(qual_details[key])
    
    return session_dict

## Event Extraction
def mnl_Extract_Event(yr,event_num,conventional_events):
    base_info, df_fp1, df_fp2, df_fp3, df_qual, weather_fp1, weather_fp2, weather_fp3, weather_qual = fastf1_extract.mnl_extract_event_data(yr, event_num, conventional_events)
    #If one of the events fails return an empty dataframe
    if (isinstance(df_fp1, bool)) | (isinstance(df_fp2, bool)) | (isinstance(df_fp3, bool)) | (isinstance(df_qual, bool)):
      if (isinstance(df_fp1, bool)):
        print(weather_fp1)
      elif (isinstance(df_fp2, bool)):
        print(weather_fp2)
      elif (isinstance(df_fp3, bool)):
        print(weather_fp3)
      elif (isinstance(df_qual, bool)):
        print(weather_qual)
      event_df = pd.DataFrame()
    else:
      driver_nums = fastf1_transform.mnl_identify_participating_drivers(df_qual) #Drivers who will participate in qualifying

      #Extract Practice data
      fp1_session = mnl_ExtractPracticeSessionData(df_fp1, weather_fp1, driver_nums, df_qual, "fp1")
      fp2_session = mnl_ExtractPracticeSessionData(df_fp2, weather_fp2, driver_nums, df_qual, "fp2")
      fp3_session = mnl_ExtractPracticeSessionData(df_fp3, weather_fp3, driver_nums, df_qual, "fp3")
      #Combine Practices
      practices = {}
      practices.update(fp1_session)
      practices.update(fp2_session)
      practices.update(fp3_session)
      #Extract Qualifying
      qualifying = mnl_ExtractQualifyingData(df_qual, weather_qual, driver_nums)
      event = {}
      event.update(base_info)
      event.update(practices)
      event.update(qualifying)
      event_df = pd.DataFrame(event)
      return event_df