import web_io
import templates

WEBSITE_REFERENCE_COL_URL = 2


def lookup(website_reference):
    # Get the Website Source URL
    website_url = website_reference[WEBSITE_REFERENCE_COL_URL]

    # Find the template(s) that matched the URL
    website_meta_records = templates.find_matches(website_url)

    # If no templates are found for the URL, then return an error
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


