# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# web_io.py
#
# Contains the logic for accessing and parsing websites for information
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
import re
from app import file_io
from requests import RequestException
from requests_html import HTMLSession


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Get Website Source
# Look up the root domain of the given URL and fetch the title of the home page.
# While the title might not be the exact name of the source, it will be close.
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def get_website_source(url):
    # Get the root domain name of the url
    regex_root_domain_pattern = 'https*://.*\.\w\w(\w*)(:\d\d(\d*))*/'
    regex_root_domain = re.compile(regex_root_domain_pattern, re.IGNORECASE)
    root_domain = regex_root_domain.search(url).group()

    # Fetch the title
    website = get_website(root_domain)
    return website.get('title')


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Get Website
# Download the website and pull out meaningful data
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def get_website(url):
    session = HTMLSession()

    try:
        page = session.get(url)
    except RequestException as err:
        print('     ' + str(err))
        return {
            'status_code': 500,
            'title': '',
            'links': []
        }

    attributes = {
        'status_code': page.status_code
    }

    if 200 == page.status_code:
        try:
            # Title
            page_title = page.html.find('head > title', first=True)
            if page_title:
                attributes['title'] = file_io.clean_txt(page_title.text)

            # Meta Keywords
            meta_tags = page.html.find('head > meta')
            if meta_tags:
                _append_meta_tags(attributes, meta_tags)

            # Links
            page_links = page.html.absolute_links
            if page_links:
                attributes['links'] = page_links

        except UnicodeDecodeError:
            print('      ** Error processing URL ' + url)
            if not attributes.get('title'):
                attributes['title'] = ''
            if not attributes.get('links'):
                attributes['links'] = []
    else:
        attributes['title'] = ''
        attributes['links'] = []

    return attributes


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Get Website Status
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def get_website_status(url):
    session = HTMLSession()
    try:
        page = session.get(url)
    except RequestException:
        return 500

    return page.status_code


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Private methods
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def _append_meta_tags(attributes, meta_tags):
    for tag in meta_tags:
        if tag.attrs.get('name'):
            tag_name = tag.attrs.get('name').strip().lower()
            if 'description' == tag_name:
                attributes['meta-description'] = file_io.clean_txt(tag.attrs.get('content'))
            elif 'keywords' == tag_name:
                attributes['meta-keywords'] = file_io.clean_txt(tag.attrs.get('content'))
