# 3rd party libraries
import yaml
import csv
import re
from requests_html import HTMLSession


def get_content_templates(file_name):
    print('Loading content templates: ', end='')

    templates_file = open(file_name, 'r')
    templates = yaml.load(templates_file)
    templates_file.close()

    for index, template in enumerate(templates):
        if index > 0:
            print(', ', end='')
        print(template['name'], end='')

    print('\n')

    return templates


def get_root_domain_url(url):
    regex_root_domain_pattern = 'https*://.*\.\w\w(\w*)/'
    regex_root_domain = re.compile(regex_root_domain_pattern, re.IGNORECASE)
    return regex_root_domain.search(url).group()


def get_website_references(csv_file_name):
    with open(csv_file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        csv_rows = list(reader)

        # remove the title row
        csv_rows.pop(0)

    return csv_rows


def get_website_attributes(url):
    session = HTMLSession()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    # Get the URL website attributes
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
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

    return attributes
