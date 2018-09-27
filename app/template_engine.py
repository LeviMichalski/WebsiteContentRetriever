# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# template_engine.py
#
# A "template engine" that will accept any website URL, look up details about the
# URL, and compare it to pre-configured templates (in templates.yaml) for
# additional static meta data for the URL.
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
import re
import yaml
from app import web_io

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Templates Supported
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
_TEMPLATE_SOURCE_URL = 'Source URL'
_TEMPLATE_WEBSITE_LINK = 'Website Link'


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# INITIALIZE: Load the templates into a local cache so that they are only loaded
# once per program execution
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
with open('./app/templates.yaml', 'r') as templates_file:
    _TEMPLATE_CACHE = yaml.load(templates_file)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Find Matches
# Look through the templates to find matches based on the template rules. This
# method could return multiple matches if the template type 'Website Link' finds
# multiple website links that match.
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def find_matches(url):
    matches = _get_source_url_matches(url)

    if not matches:
        matches = _get_website_link_matches(url)

    return matches


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Private Functions
# These functions should only be used within this file
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def _get_source_url_matches(url):
    source_url_templates = _get_templates(_TEMPLATE_SOURCE_URL)
    match = _match(source_url_templates, url)
    if match:
        return [match]  # Return as a list


def _get_website_link_matches(url):
    # Fetch the links within the source URL website. Each link found will be examined by the
    # templates for a match. If there are multiple links that match a template, then append the
    # link to another match of the same template type, otherwise create a new matched template entry.
    matches = []
    website_link_templates = _get_templates(_TEMPLATE_WEBSITE_LINK)

    source_website = web_io.get_website(url)
    website_links = source_website['links']

    for website_link in website_links:
        match = _match(website_link_templates, website_link)
        if match:
            # TODO: append to an existing record if the template is the same
            match['url'] = url
            match['url_status'] = source_website.get('status_code')
            match['fmi_link'] = website_link
            matches.append(match)

    return matches


def _get_templates(template_name):
    templates = []
    for template in _TEMPLATE_CACHE:
        if template_name.lower() == template['search']['type'].lower():
            templates.append(template)
    return templates


def _match(templates, url):
    for template in templates:
        search_criteria = template['search']['contains'].split(',')
        if _search(url, search_criteria):
            match = {
                'url': url
            }

            if template.get('meta'):
                match['source'] = template['meta'].get('source')
                match['source-type'] = template['meta'].get('source-type')
                match['association'] = template['meta'].get('association')
                match['source-sector'] = template['meta'].get('source-sector')
                match['fmi-content-type'] = template['meta'].get('fmi-content-type')
                match['fmi-content-title'] = template['meta'].get('fmi-content-title')
                match['link-location'] = template['meta'].get('link-location')

            return match


def _search(text, search_criteria):
    # search criteria can use regular expression syntax (regex) for added power
    # https://docs.python.org/3/library/re.html
    for c in search_criteria:
        regex = re.compile(c.strip(), re.IGNORECASE)
        if regex.search(text):
            return True

    return False
