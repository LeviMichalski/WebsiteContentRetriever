# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# website_meta.py
#
# Gathers all necessary meta data relating to a website referral, including static
# data from the built-in template engine (template_engine.py).
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
from app import web_io
from app import template_engine

WEBSITE_REFERRAL_COL_URL = 2


def lookup(website_referral):
    # Get the Website Source URL
    website_url = website_referral[WEBSITE_REFERRAL_COL_URL]

    # Get static meta data from the template engine
    website_meta_records = template_engine.find_matches(website_url)
    if not website_meta_records:
        return [{
            'url': website_url,
            'error': 'No template matched'
        }]

    # Get the base website Source
    website_source = web_io.get_website_source(website_url)

    # Apply dynamic website meta data
    for website_meta in website_meta_records:

        # Source
        if not website_meta.get('source'):
            website_meta['source'] = website_source

        #   TODO source-type: searches the source URL for terms like "news", "blog", and defaults to "website"
        #   TODO fmi-link-status: validates that the FMI link is active (HTTP 200)
        #   TODO keywords: get from website content (look up the standard way of adding keywords)

    return website_meta_records


