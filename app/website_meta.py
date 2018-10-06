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
    # Get the URL
    source_url = website_referral[WEBSITE_REFERRAL_COL_URL]

    # Get the Source website content meta
    source_meta = web_io.get_website(source_url)
    source_title = web_io.get_website_source(source_url)

    #   TODO source-type: searches the source URL for terms like "news", "blog", and defaults to "website"

    # Prefix meta records with these values
    meta_prefix = {
        'published-date': website_referral[WEBSITE_REFERRAL_COL_PUBLISHED],
        'title': website_referral[WEBSITE_REFERRAL_COL_TITLE],
        'url': source_url,
        'source': source_title,
        'meta-description': source_meta.get('meta-description'),
        'meta-keywords': source_meta.get('meta-keywords')
    }

    # Get static meta data from the template engine
    website_meta_records = template_engine.find_matches(source_url, meta_prefix)
    if not website_meta_records:
        error_record = {'error': 'No template matched'}
        return [{**meta_prefix, **error_record}]

    return website_meta_records
