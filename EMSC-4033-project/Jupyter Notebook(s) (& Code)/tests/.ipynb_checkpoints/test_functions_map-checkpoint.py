from assets.functions_map import *
import pytest

def test_obtain_spKey():
    #Try different organism to see if returning vaild Key
    #animals
    data_url = "https://api.gbif.org/v1/occurrence/search?"
    name= 'Macropus rufus'
    obtain_spKey(data_url, name)
    assert type(obtain_spKey(data_url, name))==  int, " *** Error, not a vaild Key"

def test_obtain_spKey():
    #Try different organism to see if returning vaild Key
    #plants
    data_url = "https://api.gbif.org/v1/occurrence/search?"
    name= 'Abrophyllum ornans'
    obtain_spKey(data_url, name)
    assert type(obtain_spKey(data_url, name))==  int, " *** Error, not a vaild Key"

def test_obtain_spKey():
    #Try different organism to see if returning vaild Key
    #fungus
    data_url = "https://api.gbif.org/v1/occurrence/search?"
    name= 'Agaricus bisporus'
    obtain_spKey(data_url, name)
    assert type(obtain_spKey(data_url, name))==  int, " *** Error, not a vaild Key"

def test_set_up_params():
    #make sure the params are a dict containing five elements
    spKey= 2433376
    region= 'Aisa'
    limit= 300
    set_up_params(spKey, region, limit)
    assert type(set_up_params(spKey, region, limit))== dict and len(set_up_params(spKey, region, limit))== 5," *** Error, not a vaild dict"

def test_server_scan():
    #Check if the returning reponse is a tuple
    data_url="https://api.gbif.org/v1/occurrence/search?"
    offset=0
    params={'speciesKey': '2433376', 'continent': 'Oceania', 'limit': '300', 'hasCoordinate': 'true', 'hasGeospatialIssue': 'false'}
    df_main=pd.DataFrame()
    assert type(server_scan(data_url, offset, params, df_main))==tuple, " *** Error, not a vaild response"

#If this function is working, we would see a csv file being generated in the folder containing Map.ipynb.
#Below is just a type test
def test_get_csv():
    df_main=pd.DataFrame()
    assert type(get_csv(df_main))== pd.core.frame.DataFrame, " *** Error, not a vaild dataframe"

def test_basemap_source():
    assert type(basemap_source())== dict and basemap_source() != {}, " *** Error, not a dict or a empty dict" 


    


