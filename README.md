# Website Referral Lookup
Python app that will lookup website URLs and fill in preconfigured 
meta data depending on the URL or the website HTML content.

This application was originally created to automate the manual process of looking up website "hits" that 
accessed content on a corporate website. Content providers analyze these results to determine where traffic
is originating from. 


## Setup & Go
Requirements
  * Git @ https://git-scm.com
    - Download the latest version from the home page
    - If there is an option to add 'git' to the PATH, then choose to do so
  * Python 3.7 or higher @ https://www.python.org/downloads/
    - Download the latest version from the home page
    - Windows: Make sure to choose the option to add Python to the PATH on the first Setup Wizard screen.
  * pip - Python package installer (comes with Python >=3.4) 

These instructions will assume execution from an OS terminal console
window. The type of operating system should not matter, except that
you will need to [Google how to open a terminal window](http://lmgtfy.com/?q=how+do+I+open+a+terminal+window) 
if you are not already familiar.  

1. Create a project workspace for your development projects
    ```
    mkdir my-workspace
    cd workspace
    ```
     
2. Clone this project to your local workstation
   ```
   git clone https://github.com/LeviMichalski/WebsiteContentRetriever.git
   cd WebsiteContentRetriever  
   ```

3. Install dependent Python packages used by this application
    ```
    pip install PyYAML requests_html requests 
    ```

4. Run the program using the sample-content provided in the project
    ```
    python3 Main.py sample-content/demo-content.csv  
    ```
    
5. Observe the output of the application and wait approximately 2 minutes for completion
    ```
    /usr/local/bin/python3.7 /Users/tim/Documents/workspace/WebsiteContentRetriever/Main.py sample-content/demo-content.csv

    Website Referral Lookup 1.0
     - Authors: Levi Michalski, Tim Michalski

    1. Contractors expect more change in next 5 years than past 50
         {'published_date': '2018-08-22', 'title': 'Contractors expect more change in next 5 years than past 50', 'url': 'https://www.constructiondive.com/news/contractors-expect-more-change-in-next-5-years-than-past-50/530454/', 'url_status': 200, 'fmi_link': 'https://www.fminet.com/wp-content/uploads/2018/08/AGCRiskStudy_2018.pdf', 'fmi_link_status': 200, 'source': 'Construction News and Trends | Construction Dive'}
         {'published_date': '2018-08-22', 'title': 'Contractors expect more change in next 5 years than past 50', 'url': 'https://www.constructiondive.com/news/contractors-expect-more-change-in-next-5-years-than-past-50/530454/', 'url_status': 200, 'fmi_link': 'https://www.fminet.com/news/2018/08/07/fmi-releases-2018-agc-fmi-risk-management-study-managing-risk-in-the-digital-age/', 'fmi_link_status': 200, 'source': 'Construction News and Trends | Construction Dive'}

    2. How industry pressure points drive tech innovation
         {'published_date': '2018-08-22', 'title': 'How industry pressure points drive tech innovation', 'url': 'https://www.constructiondive.com/news/how-industry-pressure-points-drive-tech-innovation/530473/', 'url_status': 200, 'fmi_link': 'http://lp.fminet.com/labor-productivity-and-construction-automation-webinar-od.html', 'fmi_link_status': 200, 'source': 'Construction News and Trends | Construction Dive'}
    
    3. Make Your Construction Firm Attractive To Private Equity | HJR Global
         {'published_date': '2018-08-21', 'title': 'Make Your Construction Firm Attractive To Private Equity | HJR Global', 'url': 'https://hjrglobal.com/news/6-steps-to-make-your-construction-firm-attractive-to-private-equity/', 'url_status': 200, 'fmi_link': 'https://www.fminet.com/fmi-quarterly/article/2017/06/whats-driving-contractor-acquisition-trends/', 'fmi_link_status': 200, 'source': 'HJR Global | Helping Small Businesses Start, Grow and Expand'}
         
    ... many more rows ...
    
    200. Six things I learned at World Water Week
     {'published_date': '2017-08-31', 'title': 'Six things I learned at World Water Week', 'url': 'https://www.globalwaterintel.com/insight/six-things-i-learned-at-world-water-week', 'error': 'No template matched'}

    Writing results to sample-content/demo-content_meta-2018103-131.csv
    Website referrals processed in 13.8 minutes 
    ```

6. View the results in MS Excel 
  * Open Windows Explorer (Windows) or Finder (Mac)
  * Navigate to workspace/WebsiteContentRetriever/sample-content
  * Locate the file demo-content-test-_meta-[DATE]-[TIME].csv
    * Double click on the file if you have MS Excel installed
    * Open the file your IDE or text editor if you do not have Excel 


## How It Works
Essentially, the application examines the URLs in a CSV file and checks to see if they
match a predefined meta data template. Meta data templates contain static meta
data that is to be associated with a matching URL.

```
    URL: http://www.prnewswire.com/press-release/12345
    
    Template
    - name: Press Release
      search:
        type: Source URL
        contains: prnewswire.com
      meta:
        source: PR News Wire
        source-type: Press Release
        association: No
        source-sector: News     
``` 

In the example above, the URL found in the BuzzSumo CSV file contains 'prnewswire.com'
so this application will apply the "meta" values in the template to the URL. When
the program is done processing all of the URLS found in the CSV file, it will print
the URLs along with the meta data to a new CSV file. 

Basic outline: 
  1. Read a CSV file in the BuzzSumo format
     * Only the first 3 columns are used. All other columns are ignored
     * Published Date, Title, URL
  2. For each of the URLs in the CSV file...
     * Search the URL text to see if it matches a template
     * If a match is found, then copy the meta data for the template to the URL
     * If a match is not found...
       * Fetch the website at the URL and extract out all of the links
       * Search the link text to see if it matches a template (just like the URL from the CSV file)
       * If a match is found, then copy the meta data for the template to the URL 
  3. Write the meta data to a new CSV file
     * The file name will be the original file name + a date and time stamp. For example: BuzzSumo-20181002-1253.csv
     * The first 3 columns of the original file are copied into the first 3 columns of the new file (Published Date, Title, URL)
     * All meta data copied to the URL is written into the subsequent columns


## Templates
Templates are externalized rules that describe the type of meta data to be assigned
to matching URLs.  

### YAML Config
The default templates configuration file can be found in the root folder of the project in the file _templates.yaml_. 
The internal format of _template.yaml_ file follows [YAML](http://yaml.org/refcard.html). The expected structure of
the _templates.yaml_ file is a list of templates. For example: 

_templates.yaml_
```
    - name: Press Release
      search:
        type: Source URL
        contains: prnewswire.com
      meta:
        source: PR News Wire
        source-type: Press Release
        association: No
        source-sector: News
        
    - name: FMI Home Page
      search:
        type: Website Link
        contains: fminet.com$, fminet.com/$
      meta:
        link-location: Homepage             
``` 

A list item in YAML syntax is defined with a hyphen (-) followed by the first attribute of the 
list item (aka template), which is "name". Additional attributes of the template are 
preceded with an indent and then the attribute name. An indent in YAML indicates that the next attribute
is associated with the template definition. 

> NOTE: If any other YAML configuration is followed, the application will either ignore the extra attributes
or fail to start if expected attributes are not found.  

### Template Attributes
Each template definition has the 3 primary attributes: name, search, meta.

#### name
The name of the template. This name is not used within the application for any purpose other than
to for readers of template.yaml to identify different templates. This name field can contain any name of any length.

    - name: This is my descriptive name

#### search
The search attribute of a template only contains sub-attributes that define the "type" of search
and what the search "contains" for a successful match.

##### type: Source URL

This type of search will examine the source URL found within the CSV input file. In circumstances where
the source URL contains a domain name that is common, there is no need to examine the contents of the 
website to know what default meta data to apply to the URL. 

For example, if all press releases are posted to 'prnewswire.com', then the meta data can be applied immediately to 
that source URL without examining the contents of the prnewswire.com website URL. 

    - name: Press Release (prnewswire.com)
      search: 
        type: Source URL
        contains: prnewswire.com

##### type: Website Link

A Website Link search will examine all of the links found within the website of the source URL from the CSV file. This
search will first access the website of the source URL from the CSV file, download it, extract out all of the links, 
then check to see if the links match this type of template. 

    - name: FMI Home Page
      search: 
        type: Website Link
        contains: fminet.com$, fminet.com/$
 
 If the website link matches the 'contains' search attribute, then it will match this template. 
 
##### contains
 
The search 'contains' attribute defines the search criteria that must match in order for the template meta data to be
applied to the website link. 

This attribute can contain multiple search criteria by separating them with a comma. 

Each search criteria defined can utilize the 
[Regular Expression](https://www.rexegg.com/regex-quickstart.html) matching syntax. While this syntax can take a while
to become familiar, there are many [online tutorials](https://www.regular-expressions.info/tutorial.html) and 
[testing tools](https://www.regextester.com) to assist the learning process.   

Example:
  
    - name: FMI Home Page
      search: 
        type: Website Link
        contains: fminet.com$, fminet.com/$
 
The 'contains' attribute contains 2 search match possibilities and utilizes a few regex symbols. The first match
possibility is 'fminet.com$' and will match any website link that ends with ($) "fminet.com". The second match
possibility is 'fminet.com/$' and will match any website link that ends with ($) "fminet.com/". In this scenario,
some website links might contain a trailing forward slash, which is equivalent to a link that doesn't have the forward
slash.  


#### meta
The meta attribute contains data that will be associated with any URL/Link that matches the search. There
are no defined meta data attributes. Whatever is placed within the meta section will be converted into columns
within the CSV output results. 

For example:

```
    - name: Press Release
      search:
        type: Source URL
        contains: prnewswire.com
      meta:
        source: PR News Wire
        source-type: Press Release
        association: No
        source-sector: News
        
    - name: FMI Home Page
      search:
        type: Website Link
        contains: fminet.com$, fminet.com/$
      meta:
        link-location: Homepage             
``` 

If there are 2 results and one matches the first template and the other matches the second template, then the CSV results
file will contain the following columns:

| url                   | source       | source-type   | association | source-sector | link-location |
|-----------------------|--------------|---------------|-------------|---------------|---------------|
| http://prnewswire.com | PR News Wire | Press Release | No          | News          |               |
| http://fminet.com     | FMI          |               |             |               | Homepage      |

The final CSV results will contain a column for each of the meta data found within the _template.yaml_ file regardless
 of whether the meta data matched a URL/Link. CSV results files that contain the same exact columns for each program
 execution will be easier to compare.  

#### Computed Results
The following columns will be added to the CSV results for each URL that matched a template. 

  * **url_status**: the [HTTP Status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) response code of the Source URL from the CSV file
  * **content_link**: the matching link found within the source URL website content
  * **content_link_status**: the [HTTP Status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) response code of the website content link
  * **source**: the website page title of the root domain of the source URL or website link. This value can be overridden by specifying it in the meta data of the template.
  * **error**: any error message that was generated while processing the source URL record 

### _templates.yaml_ locations
The default location for the _templates.yaml_ file is in the root project folder. You can choose to
modify the _templates.yaml_ file in the root project folder, but the changes will be overwritten any
time the project is updated through Git. Alternatively, your team can choose to commit all changes
to Git for sharing with team members and permanent storage.

To personalize your templates without affecting the Git source code, this application will first look
for the _templates.yaml_ file in the following locations:
 
    1. HOME_FOLDER/templates.yaml
    2. HOME_FOLDER/WebsiteContentRetriever/templates.yaml
    3. PROJECT_ROOT_FOLDER/templates.yaml   

For example, if on a Windows 10 machine, the _templates.yaml_ lookup path for me would be:

    1. C:\Users\Tim Michalski\templates.yaml
    2. C:\Users\Tim Michalski\WebsiteContentRetriever\templates.yaml
    3. C:\Users\Tim Michalski\Documents\python-workspace\WebsiteContentRetriever\templates.yaml
