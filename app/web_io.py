# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# web_io.py
#
# Contains the logic for accessing and parsing websites for information
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
import re
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
    page = session.get(url)

    attributes = {
        'status_code': page.status_code
    }

    if 200 == page.status_code:
        try:
            page_title = page.html.find('head > title', first=True)
            if page_title:
                attributes['title'] = page_title.text

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
