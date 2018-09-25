# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Website Content Retriever
#
# Examines a source URL to determine which type of content that it's referencing.
#
# Authors: Levi Michalski, Tim Michalski
# License: Apache 2.0
# GitHub: https://github.com/LeviMichalski/WebsiteContentRetriever
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# !! WARNING !!   -- Tim Michalski  9/24/2018
# A known issue exists where this program will fail when a CSV file contains
# Microsoft specific double quote characters.
#
# For example: “Musts”
#
# The begin and end quotes are not unicode and will throw an exception. Before
# creating a CSV file, consider doing a find and replace on the file for these
# begin and end quotes and replace with a single quote like '
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


import sys
import search
import time
import data_access

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Application Parameters
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
COLUMN_TITLE = 1
COLUMN_URL = 2
TEMPLATES_CONFIG_FILE = 'templates.yaml'

HTTP_STATUS_OK = 200
HTTP_STATUS_FORBIDDEN = 403
HTTP_STATUS_NOT_FOUND = 404

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Welcome Message
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
print()
print('Website Content Retriever 1.0')
print(' - Authors: Levi Michalski, Tim Michalski')
print()

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Command Line Arguments
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
if len(sys.argv) == 1:
    print("ERROR: Please enter the name of the .CSV file to process.")
    print("Example: Main.py sample-content/demo-content.csv")
    quit()

website_references_file = sys.argv[1]

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Load Reference Templates
#
# These templates will be used to determine how to fill in the columns of data associated with each website
# reference record.
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
templates = data_access.get_content_templates(TEMPLATES_CONFIG_FILE)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Load Reference Templates
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
website_references = data_access.get_website_references(website_references_file)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Process Website References
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
start_time = time.time()

for index, website_reference in enumerate(website_references):
    title = website_reference[COLUMN_TITLE]
    url = website_reference[COLUMN_URL]

    print(str(index+1) + '. ' + title)
    print('      URL: ' + url)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    # Fetch the company name from the root domain page title
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    root_domain_url = data_access.get_root_domain_url(url)
    root_domain_attributes = data_access.get_website_attributes(root_domain_url)
    print('      ' + root_domain_attributes.get('title'))

    # examine templates
    template_matched = False
    for template in templates:
        if template_matched:
            break

        # Source URL
        if 'Source URL' == template['search']['type']:
            url_search_criteria = template['search']['contains']
            if search.find_text(url, url_search_criteria):
                print('      ' + template['name'] + ' match')
                template_matched = True

        elif 'URL In Source Content' == template['search']['type']:
            url_search_criteria = template['search']['contains']

            website_attributes = data_access.get_website_attributes(url)
            if HTTP_STATUS_OK == website_attributes['status_code']:
                for link in website_attributes['links']:
                    if search.find_text(link, url_search_criteria):
                        print('      ' + template['name'] + ': ' + link)
                        template_matched = True

            elif HTTP_STATUS_NOT_FOUND == website_attributes['status_code']:
                print('      CHECK MANUALLY: The URL no longer exists or is not accessible.')
                template_matched = True

            elif HTTP_STATUS_FORBIDDEN == website_attributes['status_code']:
                print('      CHECK MANUALLY: This link is blocking this program. Verify manually.')
                template_matched = True

            else:
                print('      LINK ERROR: Link not accessible for some reason (HTTP status code = ' + str(website_attributes['status_code']) + ')')
                template_matched = True

    if not template_matched:
        print('      NO MATCH')

    print()


elapsed_time = round((time.time() - start_time)/60, 1)  # minutes rounded to the nearest tenth
print('Website references processed in ' + str(elapsed_time) + ' minutes')

#     1. Setup - load config/template files

# import the YAML library
# open the settings.yaml file
# read the single setting in the file
# close the settings.yaml file


#     2. Load the CSV with URLs & content

# a. import a CSV reader

# b. input parameter to get the name of the file
#   python Main.py my-file.csv

# c. validate the columns of the file
#       - does it have a URL column?
#       - does it have all of the other required columns?


#     3. Iterate through the URLs & execute the templates

# a. for each CSV row, get the URL

# b. iterate through each of the templates to see if the MATCH is TRUE
#   If so, then complete the template fields

# c. write the template field content to a new CSV file
#   my-file-retrieved-2018-09-23-1553.csv

# d. close the files and exit

# 4. Create functions to dynamically lookup a few of the template fields (source, source type)
