import glob
import numpy as np
import pandas as pd
import geopandas as gpd
from fuzzywuzzy import fuzz
from shapely.geometry import shape, Point


def create_query_geo_df(query_file):
    """Add geometry to the query points by converting lon/lat into Shapely Points.
    """
    query_points = pd.read_csv(query_file)
    query_points.sort_values(by='STATE', inplace=True)

    # Create a Point object and add to dataframe. Convert to Geopandas Dataframe
    geometry = [Point(xy) for xy in zip(query_points['LONGITUDE'], query_points['LATITUDE'])]
    crs = {'init': 'epsg:4326'}
    query_df = gpd.GeoDataFrame(query_points, crs=crs, geometry=geometry)
    
    return query_df


def generate_state_zipcode_files(states):
    """Match the state to the appropriate zipcode geojson file. Use once only,
    but should still be a function."""
    zip_code_files = glob.glob('../data/State-zip-code-GeoJSON/*.json')
    state_zipcode_files = {}
    for state in states:
        similarity = []
        for zip_code_file in zip_code_files:
            query_state_name = '_'.join(state.lower().split(' '))
            state_name = '_'.join(zip_code_file.split('/')[-1].split('_')[:3]).lower()
            token_sort_ratio = fuzz.token_set_ratio(query_state_name, state_name)
            similarity.append(token_sort_ratio)
        closest_match = zip_code_files[similarity.index(max(similarity))]
        state_zipcode_files[state] = closest_match
    return state_zipcode_files


def append_zipcode(query_df, state, state_zipcode_files):
    """Add zipcode to the query points. 
    Group by states and read in the corresponding zipcode polygon files. 
    For each point loop through all the zip codes in the state and check
    whether it belongs to one. Save the zipcode if found.
    
    """
    query_state = query_df[query_df.STATE == state]
    print(state)
    zip_geo_file = state_zipcode_files[state]
    zip_geo_df = gpd.read_file(zip_geo_file)
    zip_codes = []
    for point in query_state.geometry:
        correct_zip = np.nan
        for i, poly in zip_geo_df[['GEOID10', 'geometry']].iterrows():
            if poly['geometry'].contains(point):
                correct_zip = poly['GEOID10']
                break
        zip_codes.append(correct_zip)
    query_state['ZIPCODE'] = zip_codes
    return query_state.drop(columns=['geometry'])


if __name__ == '__main__':
    query_file = '../data/storm_coordinates.csv'  
    
    query_df = create_query_geo_df(query_file)
    states = query_df.STATE.unique()
    state_zipcode_files = generate_state_zipcode_files(states)
    for state in states[1:]:
        with_zipcode_df = append_zipcode(query_df, state, state_zipcode_files)
        with_zipcode_df.to_csv('../output/{}_events.csv'.format(state), index=False)
    

