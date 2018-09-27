# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Website References Lookup
#
# Examines a website reference URL to determine which type of content that it's referencing and the links that are
# being referenced. Includes a template engine that will determine meta data for each reference based on the URLs.
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
import time
import file_io
import website_meta


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Welcome Message
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
print()
print('Website References Lookup 1.0')
print(' - Authors: Levi Michalski, Tim Michalski')
print()

start_time = time.time()


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Command Line Arguments
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
if len(sys.argv) == 1:
    print("ERROR: Please enter the name of the .CSV file to process.")
    print("Example: Main.py sample-content/demo-content.csv")
    quit()

website_references_file = sys.argv[1]


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Process Website References
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
_TITLE = 1

record_count = 0
website_meta_results = []

website_references = file_io.get_website_references(website_references_file)
for website_reference in website_references:

    # Print the record number and title to the console
    record_count += 1
    print(str(record_count) + '. ' + website_reference[_TITLE])

    # Look up the meta data for the website reference
    results = website_meta.lookup(website_reference)
    for result in results:
        print('     ' + str(result))
    print()

    # Append the results (could be more then 1 row) to the master list
    website_meta_results.extend(results)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Export Results to CSV
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# TODO generate a new CSV file name from the given name
print('Writing results to ' + 'test-results.csv')

# TODO Write the results to the CSV file
# file_io.csv_export(website_meta_results)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Elapsed time
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
elapsed_time = round((time.time() - start_time)/60, 1)  # minutes rounded to the nearest tenth
print('Website references processed in ' + str(elapsed_time) + ' minutes')
