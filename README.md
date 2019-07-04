# Storms-analysis

Using the NOAA extreme weather data to estimate probability of tornado/hail storm/hurricane per US zip code.

## Data 
Can be downloaded from the following websites

- [Raw NOAA](https://www2.ncdc.noaa.gov/pub/data/swdi/stormevents/csvfiles/) as `csv` files.
- [US Zip code](https://github.com/OpenDataDE/State-zip-code-GeoJSON) as `geojson` files. You can open these using the Python `geopandas` library.
## SQL scripts
- Files in `sql` can extract subsets of data for analysis. Should be fairly self explanatory.

## Scripts in `ipynb`
These load the data into a SQL database and performs some preliminary analysis
- `Write-to-Postgres.ipynb` reads CSV files into SQL tables.
- `Initial Visualisations.ipynb` plots some aggregate features.

## Pythons scripts
- `add_zipcode.py` queries the Zipcode GeoJson Polygons to find the zipcode for each storm point. Need to download the US Zip code file into the `data/` directory and unzip. 
