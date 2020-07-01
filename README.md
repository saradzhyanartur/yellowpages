# Python YellowPages Scraper

## Description & Implementation
A simple scraper that returns data from https://www.yellowpages.com/ in dictionary format. The package exposes the YellowPages object which
contains two methods. 

The '''get_search_results''' method corresponds to doing a basic search on yellowpages and returns a list of results with basic information.

The '''get_details''' method corresponds to looking a page for a particular buisness and returns a dictionary with detailed information. 
## Usage
``` python
from yellowpages import YellowPages

client = YellowPages()


results = client.get_search_results(search_terms = 'Bars', location_city='Boston', 
                                                    location_state='MA', page_range=(0,2))


for result in results:
    url_extension = result['url_extension']
    details = client.get_details(url_extension=url_extension)
    print(details)
```
