import fastf1 as ff1
import pandas as pd
import numpy as np
from FastF1_DataAccess import fastf1_extract

def mnl_find_softest_compound(df):
    # Calculate the amount of laps on the softest compound
    if (df['Compound']=='SOFT').sum() > 0:
        num_laps = (df['Compound']=='SOFT').sum()
        softest_compound = 'SOFT'
    elif (df['Compound']=='MEDIUM').sum() > 0:
        num_laps = (df['Compound']=='MEDIUM').sum()
        softest_compound = 'MEDIUM'
    elif (df['Compound']=='HARD').sum() > 0:
        num_laps = (df['Compound']=='HARD').sum()
        softest_compound = 'HARD'
    elif (df['Compound']=='INTERMEDIATE').sum() > 0:
        num_laps = (df['Compound']=='INTERMEDIATE').sum()
        softest_compound = 'INTERMEDIATE'
    elif (df['Compound']=='WET').sum() > 0:
        num_laps = (df['Compound']=='WET').sum()
        softest_compound = 'WET'
    else:
        softest_compound = 'NA'
        num_laps = 0
    return softest_compound, num_laps

def mnl_get_fastest_session_times(df):
    fastest_session_data = {
        'fastest_sector1': df['Sector1Time'].min().total_seconds(),
        'fastest_sector2': df['Sector2Time'].min().total_seconds(),
        'fastest_sector3': df['Sector3Time'].min().total_seconds(),
        'fastest_lap': df['LapTime'].min().total_seconds(),
        'theorestical_fastest_lap' : df['Sector1Time'].min().total_seconds() + df['Sector2Time'].min().total_seconds() + df['Sector3Time'].min().total_seconds()
    }
    return fastest_session_data
def mnl_generate_empty_driver_session():
    driver_session_data = {
            'driver': "NA",
            'driver_num': "NA",
            'team_name': "NA",
            #fastest lap data
            'fastest_lap_compound': "NA",
            'fastest_sector1': np.nan,
            'fastest_sector2': np.nan,
            'fastest_sector3': np.nan,
            'fastest_lap': np.nan,
            'theorestical_fastest_lap': np.nan,
            'fastest_lap_num': np.nan,
            'fastest_lap_fresh_tyre': "NA",
            'fastest_lap_pit_out_time': np.nan,
            'fastest_lap_start_time': np.nan,
            'fastest_lap_warm_up': np.nan,
            'fastest_lap_speed_I1': np.nan,
            'fastest_lap_speed_I2': np.nan,
            'fastest_lap_speed_FL': np.nan,
            'fastest_lap_speed_ST': np.nan,
            'fastest_lap_track_status': "NA",
            'fastest_lap_is_accurate': "NA",
            #relative data
            'fastest_lap_to_session_fastest': np.nan,
            'fastest_lap_to_session_theorectical': np.nan,
            'theorectical_fastest_lap_to_session_fastest': np.nan,
            'theorectical_fastest_lap_to_session_theorectical': np.nan,
            'fastest_sector1_to_session_fastest': np.nan,
            'fastest_sector2_to_session_fastest': np.nan,
            'fastest_sector3_to_session_fastest': np.nan,       
            #average data
            'mean_lap': np.nan,
            'mean_lap_genuine': np.nan,
            'mean_lap_softest': np.nan,
            'mean_lap_genuine_softest': np.nan,

            'mean_lap_to_driver_fastest': np.nan,
            'mean_lap_to_driver_theorectical_fastest': np.nan,
            'mean_lap_to_session_fastest': np.nan,
            'mean_lap_to_theorectical_session_fastest': np.nan,
        
            'mean_sector1': np.nan,
            'fastest_sector1_softest': np.nan,
            'fastest_sector1_softest_to_driver_fastest': np.nan,
            'fastest_sector1_softest_to_session_fastest': np.nan,
            'fastest_sector1_genuine_softest': np.nan,
            'fastest_sector1_genuine_softest_to_driver_fastest': np.nan,
            'fastest_sector1_genuine_softest_to_session_fastest': np.nan,
        
            'mean_sector2': np.nan,
            'fastest_sector2_softest': np.nan,
            'fastest_sector2_softest_to_driver_fastest': np.nan,
            'fastest_sector2_softest_to_session_fastest': np.nan,
            'fastest_sector2_genuine_softest': np.nan,
            'fastest_sector2_genuine_softest_to_driver_fastest': np.nan,
            'fastest_sector2_genuine_softest_to_session_fastest': np.nan,

            'mean_sector3': np.nan,
            'fastest_sector3_softest': np.nan,
            'fastest_sector3_softest_to_driver_fastest': np.nan,
            'fastest_sector3_softest_to_session_fastest': np.nan,
            'fastest_sector3_genuine_softest': np.nan,
            'fastest_sector3_genuine_softest_to_driver_fastest': np.nan,
            'fastest_sector3_genuine_softest_to_session_fastest': np.nan,

            #weather
            'fastest_lap_air_temp': np.nan,
            'fastest_lap_humidity': np.nan,
            'fastest_lap_pressure': np.nan,
            'fastest_lap_rainfall': "NA",
            'fastest_lap_tack_temp': np.nan,
            'fastest_lap_wind_direction': np.nan,
            'fastest_lap_wind_speed': np.nan
        }
    return driver_session_data
    
def mnl_get_driver_session_details(df, df_weather, fastest_session_data, driver_name, driver_num, driver_team):
    df_genuine = df[df['Deleted']==False]
    df_genuine = df_genuine[df_genuine['LapTime'].isna()==False]
    if df_genuine.empty:
        driver_session_data = mnl_generate_empty_driver_session()
        driver_session_data['driver'] = driver_name
        driver_session_data['driver_num'] = driver_num
        driver_session_data['driver_team'] = driver_team
    else:       
        fastest_lap_idx = df_genuine['LapTime'].argmin()
        theorectical_fastest = df['Sector1Time'].min().total_seconds() + df['Sector2Time'].min().total_seconds() + df['Sector3Time'].min().total_seconds()
        softest = mnl_find_softest_compound(df)
        #Calculate the warm up lap
        if pd.isnull(df.iloc[fastest_lap_idx-1]['Sector1Time']):
            warm_up_lap = df.iloc[fastest_lap_idx]['LapStartTime'].total_seconds() - df.iloc[fastest_lap_idx-1]['PitOutTime'].total_seconds()
        else:
            warm_up_lap = df.iloc[fastest_lap_idx-1]['LapTime'].total_seconds()

        #Get weather index
        start_time = df.iloc[fastest_lap_idx]['LapStartTime']
        time_diff = abs(df_weather['Time'] - start_time)
        time_idx = np.argmin(time_diff)

        #Results dictionary
        driver_session_data = {
            #base info
            'driver': df.iloc[0]['Driver'],
            'driver_num': df.iloc[0]['DriverNumber'],
            'team_name': df.iloc[0]['Team'],

            #fastest lap data
            'fastest_lap_compound': df.iloc[fastest_lap_idx]['Compound'],
            'fastest_sector1': df['Sector1Time'].min().total_seconds(),
            'fastest_sector2': df['Sector2Time'].min().total_seconds(),
            'fastest_sector3': df['Sector3Time'].min().total_seconds(),
            'fastest_lap': df['LapTime'].min().total_seconds(),
            'theorestical_fastest_lap' : theorectical_fastest,
            'fastest_lap_num': df.iloc[fastest_lap_idx]['LapNumber'],
            'fastest_lap_fresh_tyre': df.iloc[fastest_lap_idx]['FreshTyre'],
            'fastest_lap_pit_out_time': df.iloc[fastest_lap_idx-1]['PitOutTime'].total_seconds(),
            'fastest_lap_start_time': df.iloc[fastest_lap_idx]['LapStartTime'].total_seconds(),
            'fastest_lap_warm_up': warm_up_lap,
            'fastest_lap_speed_I1': df.iloc[fastest_lap_idx]['SpeedI1'],
            'fastest_lap_speed_I2': df.iloc[fastest_lap_idx]['SpeedI2'],
            'fastest_lap_speed_FL': df.iloc[fastest_lap_idx]['SpeedFL'],
            'fastest_lap_speed_ST': df.iloc[fastest_lap_idx]['SpeedST'],
            'fastest_lap_track_status': df.iloc[fastest_lap_idx]['TrackStatus'],
            'fastest_lap_is_accurate': df.iloc[fastest_lap_idx]['IsAccurate'],

            #relative data
            'fastest_lap_to_session_fastest': df['LapTime'].min().total_seconds() / fastest_session_data['fastest_lap'],
            'fastest_lap_to_session_theorectical': df['LapTime'].min().total_seconds() / fastest_session_data['theorestical_fastest_lap'],
            'theorectical_fastest_lap_to_session_fastest': theorectical_fastest / fastest_session_data['fastest_lap'],
            'theorectical_fastest_lap_to_session_theorectical': theorectical_fastest / fastest_session_data['theorestical_fastest_lap'],
            'fastest_sector1_to_session_fastest': df['Sector1Time'].min().total_seconds() / fastest_session_data['fastest_sector1'],
            'fastest_sector2_to_session_fastest': df['Sector2Time'].min().total_seconds() / fastest_session_data['fastest_sector2'],
            'fastest_sector3_to_session_fastest': df['Sector3Time'].min().total_seconds() / fastest_session_data['fastest_sector3'],

            #average data
            'mean_lap': df['LapTime'].mean().total_seconds(),
            'mean_lap_genuine': df_genuine['LapTime'].mean().total_seconds(),
            'mean_lap_softest': df[df['Compound'] == softest[0]]['LapTime'].mean().total_seconds(),
            'mean_lap_genuine_softest': df_genuine[df_genuine['Compound'] == softest[0]]['LapTime'].mean().total_seconds(),

            'mean_lap_to_driver_fastest': df['LapTime'].mean().total_seconds() / df['LapTime'].min().total_seconds(),
            'mean_lap_to_driver_theorectical_fastest': df['LapTime'].mean().total_seconds() / theorectical_fastest,
            'mean_lap_to_session_fastest': df['LapTime'].mean().total_seconds() / fastest_session_data['fastest_lap'],
            'mean_lap_to_theorectical_session_fastest': df['LapTime'].mean().total_seconds() / fastest_session_data['theorestical_fastest_lap'],

            'mean_sector1': df['Sector1Time'].mean().total_seconds(),
            'fastest_sector1_softest': df[df['Compound'] == softest[0]]['Sector1Time'].min().total_seconds(),
            'fastest_sector1_softest_to_driver_fastest': df[df['Compound'] == softest[0]]['Sector1Time'].min().total_seconds() / df['Sector1Time'].min().total_seconds(),
            'fastest_sector1_softest_to_session_fastest': df[df['Compound'] == softest[0]]['Sector1Time'].min().total_seconds() / fastest_session_data['fastest_sector1'],
            'fastest_sector1_genuine_softest': df_genuine[df_genuine['Compound'] == softest[0]]['Sector1Time'].min().total_seconds(),
            'fastest_sector1_genuine_softest_to_driver_fastest': df_genuine[df_genuine['Compound'] == softest[0]]['Sector1Time'].min().total_seconds() / df['Sector1Time'].min().total_seconds(),
            'fastest_sector1_genuine_softest_to_session_fastest': df_genuine[df_genuine['Compound'] == softest[0]]['Sector1Time'].min().total_seconds() / fastest_session_data['fastest_sector1'],

            'mean_sector2': df['Sector2Time'].mean().total_seconds(),
            'fastest_sector2_softest': df[df['Compound'] == softest[0]]['Sector2Time'].min().total_seconds(),
            'fastest_sector2_softest_to_driver_fastest': df[df['Compound'] == softest[0]]['Sector2Time'].min().total_seconds() / df['Sector2Time'].min().total_seconds(),
            'fastest_sector2_softest_to_session_fastest': df[df['Compound'] == softest[0]]['Sector2Time'].min().total_seconds() / fastest_session_data['fastest_sector2'],
            'fastest_sector2_genuine_softest': df_genuine[df_genuine['Compound'] == softest[0]]['Sector2Time'].min().total_seconds(),
            'fastest_sector2_genuine_softest_to_driver_fastest': df_genuine[df_genuine['Compound'] == softest[0]]['Sector2Time'].min().total_seconds() / df['Sector2Time'].min().total_seconds(),
            'fastest_sector2_genuine_softest_to_session_fastest': df_genuine[df_genuine['Compound'] == softest[0]]['Sector2Time'].min().total_seconds() / fastest_session_data['fastest_sector2'],

            'mean_sector3': df['Sector3Time'].mean().total_seconds(),
            'fastest_sector3_softest': df[df['Compound'] == softest[0]]['Sector3Time'].min().total_seconds(),
            'fastest_sector3_softest_to_driver_fastest': df[df['Compound'] == softest[0]]['Sector3Time'].min().total_seconds() / df['Sector3Time'].min().total_seconds(),
            'fastest_sector3_softest_to_session_fastest': df[df['Compound'] == softest[0]]['Sector3Time'].min().total_seconds() / fastest_session_data['fastest_sector3'],
            'fastest_sector3_genuine_softest': df_genuine[df_genuine['Compound'] == softest[0]]['Sector3Time'].min().total_seconds(),
            'fastest_sector3_genuine_softest_to_driver_fastest': df_genuine[df_genuine['Compound'] == softest[0]]['Sector3Time'].min().total_seconds() / df['Sector3Time'].min().total_seconds(),
            'fastest_sector3_genuine_softest_to_session_fastest': df_genuine[df_genuine['Compound'] == softest[0]]['Sector3Time'].min().total_seconds() / fastest_session_data['fastest_sector3'],

            #weather
            'fastest_lap_air_temp': df_weather.iloc[time_idx]['AirTemp'],
            'fastest_lap_humidity': df_weather.iloc[time_idx]['Humidity'],
            'fastest_lap_pressure': df_weather.iloc[time_idx]['Pressure'],
            'fastest_lap_rainfall': df_weather.iloc[time_idx]['Rainfall'],
            'fastest_lap_tack_temp': df_weather.iloc[time_idx]['TrackTemp'],
            'fastest_lap_wind_direction': float(df_weather.iloc[time_idx]['WindDirection']),
            'fastest_lap_wind_speed': df_weather.iloc[time_idx]['WindSpeed']
        }  
    return driver_session_data

def mnl_identify_participating_drivers(df):
    driver_nums = list(df['DriverNumber'].unique())
    return driver_nums

def mnl_get_driver_and_teammate_dataframes(df, DriverNum,df_qual):
    Driver_df = df[df['DriverNumber']==str(DriverNum)]
    if not Driver_df.empty:
        Team = Driver_df.iloc[0]['Team']
        Team_df = df[df['Team']==Team]
        TeamMate_df = Team_df[Team_df['DriverNumber']!=str(DriverNum)]
    else:
        print(f"Driver Numer {DriverNum} didn't take part, deriving data from qualifying template")
        Team = df_qual[df_qual['DriverNumber']==str(DriverNum)].iloc[0]['Team']
        TeamMate_df = df[df['Team']==Team]
        t_df = df_qual[df_qual['DriverNumber']==DriverNum]
        temp_dict = {
            'Driver': [t_df.iloc[0]['Driver']],
            'DriverNumber': [t_df.iloc[0]['DriverNumber']],
            'Team': [t_df.iloc[0]['Team']],
            'Deleted': [True], #Adding this as a marker so downstream code knows to fill driver details with NaN
            'LapTime': [np.nan]        
        }
        Driver_df = pd.DataFrame(temp_dict)
        
    return Driver_df, TeamMate_df

def mnl_compare_drivers(driver_session_data, teammate_session_data):
    keys = driver_session_data.keys()
    comparison_data = {}
    for key in keys:
        if isinstance(driver_session_data[key], float) or isinstance(driver_session_data[key], int) or (driver_session_data[key]==np.nan):
            col_name = key + "_diff_to_teammate"
            if driver_session_data[key]==np.nan:
                print(f"{key} is a {np.nan}")
            comparison_data[col_name] = driver_session_data[key]-teammate_session_data[key]
    return comparison_data

def mnl_concat_dictionaries(driver_session_data, teammate_session_data, comparison_data):
    driver_all = {}
    driver_all.update(driver_session_data)
    cols = ['driver','driver_num','team_name']
    for col in cols:
        teammate_session_data.pop(col)
    driver_all.update(teammate_session_data)
    driver_all.update(comparison_data)
    return driver_all

def mnl_add_session_prefix(driver_all, prefix):
    driver_session = {}
    keys = driver_all.keys()
    for key in keys:
        new_key = prefix + "_" + key
        driver_session[new_key] = driver_all[key]
    return driver_session

def mnl_update_session_dictionary(session_dict, driver_session):
    keys = driver_session.keys()
    for key in keys:
        if key in session_dict:
            try:
                session_dict[key].append(driver_session[key])
            except:
                print(f"Problem is this key: {key}")
        else:            
            session_dict[key] = driver_session[key]
    return session_dict

def mnl_get_fastest_qualifying_lap(df, df_weather, driver_num):
    df_driver = df[df['DriverNumber']==driver_num]
    #Only count valid laps
    df_genuine = df_driver[df_driver['Deleted']==False]
    df_genuine = df_genuine[df_genuine['LapTime'].isna()==False]
    if df_genuine.empty:
        qual_dict = {
            #Driver Info
            'qual_driver_num': driver_num,
            'qual_driver': df_driver.iloc[0]['Driver'],
            #weather
            'qual_air_temp': np.nan,
            'qual_humidity': np.nan,
            'qual_pressure': np.nan,
            'qual_rainfall': "NA",
            'qual_tack_temp': np.nan,
            'qual_wind_direction': np.nan,
            'qual_wind_speed': np.nan,
            #tyre_compound
            'qual_compound': "NA",
            #fastest lap
            'qual_time': np.nan 
        }
    else:
        fastest_lap_idx = df_genuine['LapTime'].argmin()

        #Get weather index
        start_time = df_genuine.iloc[fastest_lap_idx]['LapStartTime']
        time_diff = abs(df_weather['Time'] - start_time)
        time_idx = np.argmin(time_diff)

        qual_dict = {
            #Driver Info
            'qual_driver_num': driver_num,
            'qual_driver': df_driver.iloc[0]['Driver'],
            #weather
            'qual_air_temp': df_weather.iloc[time_idx]['AirTemp'],
            'qual_humidity': df_weather.iloc[time_idx]['Humidity'],
            'qual_pressure': df_weather.iloc[time_idx]['Pressure'],
            'qual_rainfall': df_weather.iloc[time_idx]['Rainfall'],
            'qual_tack_temp': df_weather.iloc[time_idx]['TrackTemp'],
            'qual_wind_direction': float(df_weather.iloc[time_idx]['WindDirection']),
            'qual_wind_speed': df_weather.iloc[time_idx]['WindSpeed'],
            #tyre_compound
            'qual_compound': df_genuine.iloc[fastest_lap_idx]['Compound'],
            #fastest lap
            'qual_time': df_genuine['LapTime'].min().total_seconds()   
        }
    return qual_dict