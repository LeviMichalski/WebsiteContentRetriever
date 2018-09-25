
####
# !! WARNING !!   -- Tim Michalski  9/24/2018
# A known issue exists where this program will fail when a CSV file contains Microsoft specific double quote characters.
# For example: “Musts”
# The begin and end quotes are not unicode and will throw an exception. Before creating a CSV file, consider doing a
# find and replace on the file for these begin and end quotes and replace with a single quote like '





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

import csv
import sys
from requests_html import HTMLSession


def find_links(links, domain):
    matched_links = []
    for link in links:
        if link.lower().find(domain.lower()) > -1:
            matched_links.append(link)

    return matched_links


if len(sys.argv) == 1:
    print("ERROR: Please enter the name of the .CSV file to process.")
    print("Example: Main.py sample-content/demo-content.csv")
    quit()

with open(sys.argv[1], 'r') as csv_file:
    reader = csv.reader(csv_file)
    myList = list(reader)

    # remove the title row
    myList.pop(0)

for row in myList:
    url = row[2]
    print(url)

    session = HTMLSession()
    page = session.get(url)

    links = find_links(page.html.links, 'fminet.com')
    print(links)
    print()
