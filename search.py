import re


def find_links(links, domain):
    matched_links = []
    for link in links:
        if link.lower().find(domain.lower()) > -1:
            matched_links.append(link)

    return matched_links


def find_text(text_to_search, criteria):
    criteria = criteria.split(',')

    for c in criteria:
        regex = re.compile(c.strip(), re.IGNORECASE)
        if regex.search(text_to_search):
            return True

    return False
