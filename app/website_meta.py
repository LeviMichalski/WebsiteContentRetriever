# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# website_meta.py
#
# Gathers all necessary meta data relating to a website referral, including static
# data from the built-in template engine (template_engine.py).
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
from app import web_io
from app import template_engine

WEBSITE_REFERRAL_COL_PUBLISHED = 0
WEBSITE_REFERRAL_COL_TITLE = 1
WEBSITE_REFERRAL_COL_URL = 2


def lookup(website_referral):
    # Get the Website Source URL
    website_url = website_referral[WEBSITE_REFERRAL_COL_URL]

    # Prefix meta records with these values
    meta_prefix = {
        'published_date': website_referral[WEBSITE_REFERRAL_COL_PUBLISHED],
        'title': website_referral[WEBSITE_REFERRAL_COL_TITLE],
        'url': website_url
    }

    # Get static meta data from the template engine
    website_meta_records = template_engine.find_matches(website_url, meta_prefix)
    if not website_meta_records:
        error_record = {'error': 'No template matched'}
        return [{**meta_prefix, **error_record}]

    # Get the base website Source
    website_source = web_io.get_website_source(website_url)

    # Apply dynamic website meta data
    for website_meta in website_meta_records:

        # Source
        if not website_meta.get('source'):
            website_meta['source'] = website_source

        #   TODO source-type: searches the source URL for terms like "news", "blog", and defaults to "website"
        #   TODO keywords: get from website content (look up the standard way of adding keywords)

    return website_meta_records
