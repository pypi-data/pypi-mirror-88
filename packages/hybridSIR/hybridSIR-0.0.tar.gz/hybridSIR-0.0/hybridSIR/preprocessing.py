import pandas as pd


def get_data():
    """
    Download data from JHU.
    """
    confirmed_data_df = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    recovered_data_df = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    death_data_df = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    return confirmed_data_df, recovered_data_df, death_data_df


def get_time_series_data(country_name, days_until_current=False):
    """
    Convert three .csv files from JHU to time series dataframe.
    Input is a specific countryname and days_until_current, which is
    the length of the tail of the dataframe (days until the current date),
    if specified. If not  specified, all data is used. This variable
    is useful to look closer into a specific timeframe.
    
    The function returns a converted dataframe
    """
    # Gather data
    df1, df2, df3 = get_data()

    # Select country
    country_confirmed_df = df1[df1["Country/Region"] == country_name]
    country_recovered_df = df2[df2["Country/Region"] == country_name]
    country_death_df = df3[df3["Country/Region"] == country_name]
    
    cleaned_confirmed_df = country_confirmed_df.drop(columns=['Province/State','Lat','Long']).sum(axis=0,skipna=True).to_frame()[1:]
    cleaned_recovered_df = country_recovered_df.drop(columns=['Province/State','Lat','Long']).sum(axis=0,skipna=True).to_frame()[1:]
    cleaned_death_df = country_death_df.drop(columns=['Province/State','Lat','Long']).sum(axis=0,skipna=True).to_frame()[1:]
    
    ts_df = pd.DataFrame(cleaned_confirmed_df.values, columns=['confirmed_count'])
    ts_df['recovered_count'] = cleaned_recovered_df.values
    ts_df['death_count'] = cleaned_death_df.values
    ts_df.index = cleaned_confirmed_df.index
    ts_df['active_infected'] = ts_df.confirmed_count - (ts_df.recovered_count)
    
    # Small dataset
    if days_until_current:
        ts_df = ts_df.iloc[-days_until_current:]
    return ts_df

