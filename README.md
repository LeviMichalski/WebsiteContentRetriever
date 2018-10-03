# Website Referral Lookup
Python app that will lookup website URLs and fill in preconfigured 
meta data depending on the URL or the website HTML content.

This application was originally created to automate the manual process of looking up website "hits" that 
accessed content on a corporate website. Content providers analyze these results to determine where traffic
is originating from. 


## Setup & Go
Requirements
  * Git @ https://git-scm.com
  * Python 3.7 or higher @ https://www.python.org/downloads/
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
[ to do ]