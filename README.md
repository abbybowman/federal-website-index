# Federal Website Index

The goal of this project is to assemble an accurate, up-to-date list of the `.gov` public websites of the federal government.  It turns out that there are a lot of sources to consider, but this repository will explain the process used and reference the source datasets. This effort is a part of the [Site Scanning program](https://digital.gov/site-scanning).    

The end product, a Federal Website Index, can be found [here](https://github.com/GSA/federal-website-index/blob/main/data/site-scanning-target-url-list.csv) and is automatically updated every week on Wednesday at 6pm ET.  It is then used by the Site Scanning program to serve as its list of Target URLs.  

## Background

Virtually all of the ~300 agencies that make up the US federal government maintain one or more websites (e.g. `www.state.gov`, `space.commerce.gov`). We know what `.gov` domains exist and which agency operates them because the `.gov` registry [makes this information public](https://github.com/cisagov/dotgov-data/blob/main/current-federal.csv), but that only tells us what domains exist (e.g. `state.gov`, `commerce.gov`). Each domain may actually have hundreds of distinct websites (e.g. `statecollection.census.gov` and `opportunity.census.gov`, which are each different websites than `www.census.gov`). This project tries to assemble a comprehensive list of all distinct federal websites available to the public.  

## Caveats
 
* The full extent of federal websites include not just `.gov` sites, but also `.mil` websites, a small number of `.fed.us` websites, and some number of `.com/.org/.net/etc.` websites. For practical purposes, this project does not currently include those. While it is difficult to quantify the number of federal websites on those other domains, we're able to approximate their scale and do know that `.gov` websites make up the vast majority of federal websites. Therefore, with the caveat of not including `.mil/.fed.us/.com/.org/etc` websites, this project should offer a largely complete view of the websites operated by the Federal government. 
* There are also many `.gov` domains and websites used by state, tribal, and local governments and some are included in our source data. This project excludes those by using the [list of federal .gov domains](https://github.com/cisagov/dotgov-data/blob/main/current-federal.csv) as a canonical list of the `.gov` domains (and thus websites) that are operated by the federal government.  We then remove websites from our index if they have a base domain that is not on that list of federal .gov domains.  

## Summary Of Methodology

Here's the process we use to build the website index: 
* Download, combine, and deduplicate some of the below datasets.
* Remove websites that contain [certain character strings](https://github.com/GSA/federal-website-index/blob/main/criteria/ignore-list.csv) that we've found almost always indicate a non-public website, such as `admin.` or `staging.`.
* Use the list of federal `.gov` domains to assign each website an agency and bureau
* Use the OMB list of agency and bureau codes to match and add website agency and bureau codes.  
* Remove any websites that do not have a base domain that is on the list of federal `.gov` domains.


A more detailed description of the process [can be found here](https://github.com/GSA/federal-website-index/blob/main/process/index-creation.md) - [actual source code [here](https://github.com/GSA/federal-website-index/blob/main/builder/main.py)].  

The list of datasets that are currently used to build the target URL list is [here](https://github.com/GSA/federal-website-index/blob/main/builder/config.py).  

## Datasets Used To Generate The Target URL List

* [List of Federal .Gov Domains](https://github.com/GSA/federal-website-index/blob/main/source-data/dotgov-registry-federal.md) 
* [List of Websites That Participate In The Digital Analytics Program](https://github.com/GSA/federal-website-index/blob/main/source-data/dap.md) 
* [2020 pulse.cio.gov Snapshot](https://github.com/GSA/federal-website-index/blob/main/source-data/pulse-snapshot.md)
* [Other .gov Websites](https://github.com/GSA/federal-website-index/blob/main/source-data/other-websites.md)
* [OMB Bureau/Agency Codes](https://github.com/GSA/federal-website-index/blob/main/source-data/omb-codes.md)


Other Datasets That Are Under Consideration For Use
* [Censys](https://github.com/GSA/federal-website-index/blob/main/source-data/censys.md) 
* Rapid7
* [2016 End of Term Web Archive](https://github.com/GSA/federal-website-index/blob/main/source-data/eot2016.md)
* 2020 End of Term Web Archive
* .gov Registry DNS

## Site Scanning Program Links

The [Site Scanning program](https://digital.gov/site-scanning/) automates a wide range of scans of public federal websites and generates data about website health and best practices. 

* [Program Website](https://digital.gov/site-scanning)
* [API Documentation](https://open.gsa.gov/api/site-scanning-api/)
* [Central Project Repository](https://github.com/GSA/site-scanning)
* [Program Documentation Repository](https://github.com/GSA/site-scanning-documentation)
* [Analysis Repository](https://github.com/GSA/site-scanning-analysis)
* [Site Scanning Engine Repository](https://github.com/GSA/site-scanning-engine)
* [Snapshots Repository](https://github.com/GSA/site-scanning-snapshots)
* [Extensive List of Links to Technical Details, Snapshots, Analysis Reports, and More](https://digital.gov/guides/site-scanning/technical-details/) (if in doubt, look here)

## Feedback

If you have questions or want to give feedback, please [leave an issue here](https://github.com/GSA/federal-website-index/issues) or email site-scanning@gsa.gov.  
