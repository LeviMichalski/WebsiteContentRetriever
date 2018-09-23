# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# Website Content Retriever
#
# Examines a source URL to determine which type of content that it's referencing.
#
# Authors: Levi Michalski, Tim Michalski
# License: Apache 2.0
# GitHub: https://github.com/LeviMichalski/WebsiteContentRetriever
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
import startup

startup.welcome()
startup.setup()

##### 2. Load the CSV with URLs & content

# a. import a CSV reader

# b. input parameter to get the name of the file
#   python Main.py my-file.csv

# c. validate the columns of the file
#       - does it have a URL column?
#       - does it have all of the other required columns?


##### 3. Iterate through the URLs & execute the templates

# a. for each CSV row, get the URL

# b. iterate through each of the templates to see if the MATCH is TRUE
# If so, then complete the template fields

# c. write the template field content to a new CSV file
# my-file-retrieved-2018-09-23-1553.csv

# d. close the files and exit

##### 4. Create functions to dynamically lookup a few of the template fields (source, source type)
