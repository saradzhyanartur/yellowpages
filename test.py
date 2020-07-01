from yellowpages import YellowPages

client = YellowPages()


results = client.get_search_results(search_terms = 'Bars', location_city='Boston', 
                                                    location_state='MA', page_range=(0,2))


for result in results:
    url_extension = result['url_extension']
    details = client.get_details(url_extension)
    print(details)

