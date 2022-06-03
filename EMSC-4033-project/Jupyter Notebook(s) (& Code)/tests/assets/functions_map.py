"""All the functions we need to make a map:
    - obtain_spKey()
    - set_up_params()
    - server_scan()
    - get_csv()
    - basemap_source()
"""
from .dependencies_map import *

def obtain_spKey(data_url, name):
    """look up the database and get you specieskey for your organism of interest. Alter the function to look for genusKey, familyKey, phylumKey and so on if needed. Why bother? if you search scientific name directly, you have all relevant results about this organism, some data may be unwanted. The specieskey gives data only about that species."""
    
    #Set up URL query string to the server to get the speciesKey (these coordinate and limit params would be explianed later)
    params = { 'q':f'{name}', 'hasCoordinate':'true', 'hasGeospatialIssue':'false', 'limit':'300'}
    #requests.get() sends a GET request to the database.
    resp = requests.get(data_url, params)
    #Turn response into json format, easier to manage
    resp_return=resp.json()
    #From the response, the list indices 0, the section named speciesKey is what we needed here
    spKey = resp_return['results'][0]['speciesKey']
    return spKey

def set_up_params(spKey, region, limit):
    """To set up parameters for the API query URL, return the dictionary of parameters in an arranged form"""
    #Now, set up the formal URL query string parameters, the coordinates are needed to plot a map.
    #These params works like filters, help you sort the results
    #'Limit' is a page parameter. Often, we have many pages of results in the response, so we need page parameters to tell us which page and position we are on. The max number of data on one page is the 'limit'.
    #To make a map, we needed coordinate parameters to find data with this spatial information.  
    params={'speciesKey':f'{spKey}', 'continent':f'{region}','limit':f'{limit}','hasCoordinate':'true', 'hasGeospatialIssue':'false'}
    return params

def server_scan(data_url, offset, params, df_main):
    """Assemble basic URL, page and other parameters to make the request to the server, combine multiple pages of results into one and load it into the dataframe we set already"""
    #'offset', like 'limit' is also a page parameter.
    #we start at the first page (page.1) at position 0 (offset =0), when we turn to the second page of the results (page.2), offset=limit we set (in this case, 300). Then we go to page 3, offset= limit*2 which is 600. 'limit' is the number of data in a single, while 'offset' indicates our position on pages.
    
    #Assemble the parameters
    requ_url= data_url+'&'+f'offset={offset}'
    #Send request to server and get response
    response = requests.get(requ_url, params)
    #status_code == 200 means a succesful request, ==404 means page not found.
    #endofRecords indicate if the current page is the last page, when endofRcords= True, we can stop requesting.
    if response.status_code == 200:
        dataset = response.json()
        df_part =pd.DataFrame.from_dict(dataset['results'])
        endOfRecords = dataset['endOfRecords']
        df_comb = pd.concat([df_main, df_part], sort= True)
        return endOfRecords, df_comb
    else:
        print('''404.error''')

def get_csv(df_main):
    """Convert the dataframe to csv format for plotting"""
    df_main.to_csv("Platypus_dataframe.csv") 
    return df_main

def basemap_source():
    """Load online map source into a dict"""
    mapper = {}
    ## Open and use images from mapbox_outdooor
    mapper["mapbox_outdoors"] = cimgt.MapboxTiles(map_id='outdoors-v11', access_token='pk.eyJ1IjoibG91aXNtb3Jlc2kiLCJhIjoiY2pzeG1mZzFqMG5sZDQ0czF5YzY1NmZ4cSJ9.lpsUzmLasydBlS0IOqe5JA')
    return mapper
