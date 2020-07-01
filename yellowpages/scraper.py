import bs4
from urllib3 import PoolManager
from certifi import where
from urllib.parse import urlencode
from urllib.parse import urlencode
from typing import Optional, Union

from yellowpages.bs4helpers import (
    extract_link, 
    extract_text,
    extract_all,
    prepare_cascade,
)


class YellowPages(object):

    __HOST__ = "https://www.yellowpages.com"
    https = PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=where())

    
    @classmethod
    def get_search_results(cls, search_terms: str, page_range: tuple, location_city: Optional[str] = '', 
                                location_state: Optional[str] = '', location_district: Optional[str] = '',  
                                    custom_location: Optional[str] = '', sort_by: Optional[str] = 'default', **kwargs) -> list:
        """Public method that returns search results for a specific query and location
        """
        URL_EXTENSION = "/search"
        if custom_location:
            location_string = custom_location
        else:
            location_string = f"{location_district}, {location_city}, {location_state}"

        results = []
        for page_num in range(*page_range):
            query = {
                'search_terms': search_terms,
                'geo_location_terms': location_string,
                's': sort_by,
                'page': page_num + 1
            }
            url_args = urlencode({**query, **kwargs})
            r = cls.https.request(
                method='GET',
                url = cls.__HOST__ + URL_EXTENSION + '?' + url_args,
            )
            if r.status != 200:
                continue
            html = bs4.BeautifulSoup(r.data, 'html.parser')
            results_html = html.find_all('div', class_='result')
            for result_html in results_html:
                result_obj = {
                    'buisness_name': extract_text(
                        html_object=result_html.find('a', class_="business-name")
                    ),
                    'url_extension': extract_link(
                        html_object=result_html.find('a', class_="business-name")
                    ),
                    'website': extract_link(
                        html_object=result_html.find('a', class_="track-visit-website")
                    ),
                    'phone_number': extract_text(
                        html_object=result_html.find('div', class_="phones phone primary")
                    ),
                    'street_address': extract_text(
                        html_object=result_html.find('div', class_="street-address")
                    ),
                    'locality': extract_text(
                        html_object=result_html.find('div', class_="locality")
                    ),
                    'categories': extract_all(
                        list_=prepare_cascade(result_html.find('div', class_="categories")).find_all('a'),
                        method=extract_text
                    ),
                    'page_found_on': page_num + 1,
                }
                results.append(result_obj)
        return results

    
    @classmethod
    def get_details(cls, url_extension: str, **kwargs):
        """Public method that returns a dictionary containing details about a particular buisness"""
        url_args = urlencode({**kwargs})
        print(cls.__HOST__ +  url_extension + '?' + url_args)
        r = cls.https.request(
                method='GET',
                url = cls.__HOST__ +  url_extension + '?' + url_args,
        )
        if r.status != 200:
            raise Exception('The server did not return 200!')
        html = bs4.BeautifulSoup(r.data, 'html.parser')
        result_obj = {
            'buisness_name' : extract_text(
                prepare_cascade(html.find('div', class_='sales-info')).find('h1')
            ),
            'full_address': extract_text(
                html.find('h2', class_='address')
            ),
            'phone': extract_text(
                html.find('p', class_='phone')
            ),
            'years_in_buisness': extract_text(
                prepare_cascade(html.find('div', class_='years-in-buisness')).find('div', class_='number')
            ),
            'BBB_rating': extract_text(
                html.find('dd', class_='bbb-rating')
            ),
            'buisness_hours': {
                'days': extract_text(
                    html.find('th', class_='day-label')
                ),
                'hours': extract_text(
                    html.find('td', class_='day-hours')
                )
            },
            'payment_methods': extract_text(
                html.find('dd', class_='payment')
            ),
            'alternative_names': extract_all(
                list_=prepare_cascade(html.find('dd', class_='aka')).find_all('p'),
                method=extract_text
            ),
            'email': extract_link(
                html.find('a', class_='email-buisness')
            ),
            'categories': extract_all(
                list_=prepare_cascade(html.find('dd', class_='categories')).find_all('a'),
                method=extract_text
            ),
        }
        return result_obj


