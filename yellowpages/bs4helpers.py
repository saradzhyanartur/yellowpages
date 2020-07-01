import bs4

def extract_text(html_object):
    try:
        text = html_object.text
    except:
        return None
    else:
        return text


def extract_link(html_object):
    try:
        link = html_object['href']
    except:
        return None
    else:
        return link


def extract_all(list_, method):
    extracted_items = []
    for item in list_: 
        extracted_items.append(method(item))
    return extracted_items


def prepare_cascade(func_return):
    #The point of this object is to be able to handle cascading methods from bs4
    emptySoup = bs4.BeautifulSoup('', 'html.parser')
    if func_return:
        return func_return
    else:
        return emptySoup
