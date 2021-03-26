# web-scraping
## Web scraping algorithm for FDA and Health Canada website.

Both FDA and Health Canada data follow a hierarchical organization. FDA data comprises of Chapter, Section and Subpart (Chapter > Section > Subpart). Similarly, Health Canada Data comprises of Chapter, Section and Subpart (Chapter > Section > Subpart).
While performing the extraction process, it is important to note there exists a character restriction of 32K while writing to a CSV file.

## FDA Data
FDA data is extracted from the official website:
https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/CFRSearch.cfm

Due to a hierarchy present, web crawling is used as an initial step to navigate through webpages. Web scraping is then used to extract relevant data from each webpage i.e., at each level of hierarchy. BeautifulSoup, a python HTML parser is used perform these functions.

The pseudocode to extract FDA data is:
Step 1 Build a list of pages to scrape from the base page.
Step 2 From the table structure of the page, scrape the required information.
Step 3 Write the scraped data as a row in a CSV file.
Step 4 Repeat Step 2 and Step 3 for each of the pages from the list of pages.

At the Subpart level, the CFR (Code for Federal Regulation) code and the regulation’s description is obtained. The CFR code is unique to each regulation defined by the FDA. The CFR code prior to the decimal point is referred to as FDA Part. For example, if the FDA regulation code is 211.56, FDA regulation code Part is 211. Foreign manufacturing suppliers who want to import to their products to the U.S. market, must comply with FDA good manufacturing practices under Title 21 of the Code of Federal Regulations (CFR).

## Health Canada Data
Health Canada data is extracted from the official website: https://laws-lois.justice.gc.ca/eng/regulations/c.r.c.%2C_c._870/index.html

Health Canada website provides an XML version of the regulations, creating a difference in process of extracting data from Health Canada website. The ElementTree XML API, a python XML parser is used to perform the extraction.

The pseudocode to extract Health Canada data is:
Step 1 Download the XML file of the website.
Step 2 Use Element Tree API to parse through the downloaded file.
Step 3 Extract required information from sub-sections under ‘Chapter’ main section.
Step 4 Write the extracted data as a row to a CSV file.
Step 5 Repeat Step 3 and Step 4 for each of the main sections.

Similar to the FDA data, at the Subpart level, the CRC (Consolidated Regulations of Canada) code and the regulation’s description is extracted. The CRC code is unique to each regulation defined by Health Canada.





 
 
 


