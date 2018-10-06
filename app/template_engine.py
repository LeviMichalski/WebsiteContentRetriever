# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# template_engine.py
#
# A "template engine" that will accept any website URL, look up details about the
# URL, and compare it to pre-configured templates (in templates.yaml) for
# additional static meta data for the URL.
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
import re
import yaml
from app import file_io
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
templates_file_path = file_io.get_file_path('templates.yaml')

with open(templates_file_path, 'r') as templates_file:
    _TEMPLATE_CACHE = yaml.load(templates_file)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Find Matches
# Look through the templates to find matches based on the template rules. This
# method could return multiple matches if the template type 'Website Link' finds
# multiple website links that match.
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def find_matches(url, meta_prefix):
    matches = _get_source_url_matches(url, meta_prefix)

    if not matches:
        matches = _get_website_link_matches(url, meta_prefix)

    return matches


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Private Functions
# These functions should only be used within this file
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def _get_source_url_matches(url, meta_prefix):
    source_url_templates = _get_templates(_TEMPLATE_SOURCE_URL)
    template_meta = _match(source_url_templates, url, meta_prefix)
    if template_meta:
        return [template_meta]  # Return as a list


def _get_website_link_matches(url, meta_prefix):
    # Fetch the links within the source URL website. Each link found will be examined by the
    # templates for a match. If there are multiple links that match a template, then append the
    # link to another match of the same template type, otherwise create a new matched template entry.
    matches = []
    website_link_templates = _get_templates(_TEMPLATE_WEBSITE_LINK)

    source_website = web_io.get_website(url)
    website_links = source_website.get('links')

    for website_link in website_links:
        template_meta = _match(website_link_templates, website_link, meta_prefix)
        if template_meta:
            # TODO: append the 'fmi_link' to an existing record if the template is the same
            template_meta['url_status'] = source_website.get('status_code')
            template_meta['content_link'] = website_link
            template_meta['content_link_status'] = web_io.get_website_status(website_link)
            matches.append(template_meta)

    return matches


def _get_templates(template_name):
    templates = []
    for template in _TEMPLATE_CACHE:
        if template_name.lower() == template['search']['type'].lower():
            templates.append(template)
    return templates


def _get_template_meta_keys():
    keys = []
    for template in _TEMPLATE_CACHE:
        meta = template.get('meta')
        if meta:
            keys.extend(meta.keys())
    return keys


def _match(templates, url, meta_prefix):
    for template in templates:
        search_criteria = template['search']['contains'].split(',')
        if _search(url, search_criteria):
            match = {**meta_prefix}

            meta = template.get('meta')
            if meta:
                # Iterate through all of the known template meta data to build out an identical record for every
                # URL. This will ensure that the CSV output always has the same columns in the same order for every
                # execution of this program.
                for meta_key in _get_template_meta_keys():
                    if meta.get(meta_key):
                        match[meta_key] = meta.get(meta_key)
                    else:
                        match[meta_key] = ''

            return match


def _search(text, search_criteria):
    # search criteria can use regular expression syntax (regex) for added power
    # https://docs.python.org/3/library/re.html
    for c in search_criteria:
        regex = re.compile(c.strip(), re.IGNORECASE)
        if regex.search(text):
            return True

    return False
