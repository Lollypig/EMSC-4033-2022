# Project report

## Instructions

This map is a very simple guide to making a distribution map of an organism. This project uses an open online database (In this map, we use data from GBIF). The Global Biodiversity Information Facility (GBIF) is an online database which offers biodiversity data using web services.
The project aims to send request using GBIF API, filter and gather organism occurrence data to build a data frame, eventually, converting it to a numpy array and adding it to the basemap. It involves two main components, the API query section and the plotting section.
First, we need to think an organism and a region of interest (a continent). (as a demonstration, I use platypus distribution in Oceania.)

Afterwards, we can use the obtain_spKey function to get the speciesKey for platypus, so I only get spatial occurrence data for this specific species, avoiding relevant but unwanted data. 
(if use ‘Ornithorhynchus anatinus’ as search key word may return some data for relevant relatives)

`#Get unique species ID for my organism`

`#Obtain the speciesKey for platypus, sciencific name 'Ornithorhynchus anatinus'.`

`spKey=obtain_spKey(data_url, name). `


Next, based on the API service URL, I need to add some parameters as filters to get desired platypus occurrence information from GBIF database via their API. 

The data_url is the URL of GBIF API services. 
`data_url = https://api.gbif.org/v1/occurrence/search?`

Set up some parameters for the API query 

`#Page parameter 'offset' indicate position and page, initial value set to 0.`

`offset = 0`

`#Page parameter 'limit' means the number of data present in a single page, max limit for GBIF is 300.`

`limit = 300`

`#endofRecords indicate if the current page is the last page, when endofRcords= True, we can stop requesting. Set to false to start with.`

`endOfRecords = False`

`#Create an empty dataframe for our data.`

`df_main = pd.DataFrame()`


For more details about GBIF API and parameters, please go to https://www.gbif.org/developer/summary and https://www.gbif.org/developer/occurrence

Assemble all parameters we need to make the ultimate URL to request the data. However, the returning data may be too much to fit in a single page (exceed the limit=300), often, we have multiple pages of results in response. Here we have the endofRecord==false loop function to get all the pages until the last. (Whenever move to next page, offset would become the last offset + limit.)
i.e. One first page, offset=0 (the starting position), limit=300. One second page, offset=0+limit= 0+300 (the last page contain 300 data, now we are on a new page). One third page, offset=300+limit=300+300 = 600 (now we are at position 600) ...

`params=(set_up_params(spKey, region, limit))`

`while endOfRecords == False:
    endOfRecords, df_main= server_scan(data_url, offset, params, df_main)
    offset += limit`

This may look a bit confusing. Basically, for this specific case, the request is sent for four times to obtain all the data from the server. At the last request, endOfRecords= True, the loop break. 
(i.e. 300 data is obtained in the first go, second run start at position 300, another 300 data is obtained, the third run start at 600, 300 data is obtained, the last run start at 900, the rest data is obtained; total data number 1102)

Now we have a pandas dataframe df_main about matched occurrence data of platypus. Convert it to a csv file preparing for plotting.

`#Convert the dataframe format to csv for easier management.`

`get_csv(df_main)`

The returned dataframe have lots of other information, what we need here is only the coordinate information we need.

`#The results contain lots of information, but we are only interested in coordinates here.`

`df_coordinate= df_main[['decimalLongitude', 'decimalLatitude']]`

`df_coordinate.head`

Form a NumPy array, make it easier to plot.

`#To plot, convert the data to numpy array`

`numpy_array = df_corrdinate.to_numpy()
print(numpy_array)
print(type(numpy_array))`

`map_tiles_dictionary = basemap_source()
map_tiles = map_tiles_dictionary[basemap_name]`

## Go plot!!!

`fig = plt.figure(figsize=(12, 12), facecolor="none")`

`# Create a GeoAxes in the tile's projection.
#Without it, the lon and lat would not be recogonised.
ax = plt.axes(projection=map_tiles.crs)`

`# Set the size of the map
ax.set_extent(map_extent)`

`# Add the on-demand image and resolution
ax.add_image(map_tiles, 10)`

`#prepartion on load your point data
#I transposed the numpy_arrray to make it suitable for plotting
oalon, oalat= numpy_array.T`

`#plot point data of organism distribution 
plt.scatter(oalon, oalat, linewidth=0, c='red', transform=ccrs.PlateCarree(), alpha=0.5, zorder=2)`


## List of dependencies

For the API requesting part, we need the `requests` package to send a request to the server, `JSON` package to format the data, `pandas` packages to create a data frame, `NumPy` package to form a plottable array and urlencode to rewrite information to format used for URL. For the plotting part, `cartopy` package is useful to add base map, axes and data point, and `matplotlib.pyplot` package actucally does the plotting.

## Describe testing

The testing code is trivial, which only checks if the code returns the expected data type and the number of elements. The information can be double-checked by accessing the GBIF database website.

To test `obtain_spKey()` function, I try different organisms to see if returning valid Keys by looking them up on the GBIF website.
#one animal, one plant and one fungus are tested
 
To test `set_up_params()` function, I input some elements to see if it returns a dictionary with the correct element number.
 
To test `server_scan()` function, I just check if it returns a tuple.

If `get_csv()` function is working, we would see a CSV file is generated in the folder containing Map.ipynb.

To test `asemap_source()` function, I just make sure it is a list but not empty as we have a map source loaded in already.

## Limitations / Future Improvments

The main limitation would be the overall framework best for the GBIF database and may not be applicable to other databases using different formatting and structure. The second limitation is the testing, which is too trial and vague. It does not test for some critical parts which may break the code. In class, Louis had said that I need to have some more specific tests to validate the data return is accurate and complete, but my tests did not achieve that requirement. The feature improvement can be made on add not only the geological features but also incorporating environmental factors to make a more informative and useful map. More importantly, the tests need more work.
