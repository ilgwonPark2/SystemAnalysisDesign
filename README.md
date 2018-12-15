# SystemAnalysisDesign
Term Project repository for System Analysis and Design course in ITM, Seoultech.

This term project handles the data management and analytics. It includes data collection, data storing into the data management system, and finding new interesting results from the data.

# Manual v1.3
## Environment Setting(fixxing)
### mysql version upgrade
This application uses mysql version 5.7 since json data type is supported in this version.
Since it is an important process and dangerous task, we highly recommend testing in another same virtual environment.

You can follow steps to upgrade in below link.

https://github.com/ilgwonPark2/SystemAnalysisDesign/wiki/Setting))-Mysql-version-upgrade

### python version upgrade
Our project codes are based on python3.6

So, it is necessary to install python3.6 version in the CentOS environment.

The user must not set ver 3.6 as a default version since most of softwares in Cloudera CentOs environment such as yum, Hue are work on the python 2 version.

Follow below link, then you can install ver 3.6

https://github.com/ilgwonPark2/SystemAnalysisDesign/wiki/Setting))-install-python3.6-ver 

### ELK Stack setting
**Elasticsearch version 6.4.3**

Elasticsearch setting: https://github.com/ilgwonPark2/SystemAnalysisDesign/wiki/SRS))Elastic-Search

**Logstash version 6.4.3**

Logstash setting: 
https://github.com/ilgwonPark2/SystemAnalysisDesign/wiki/Setting))Logstash 

**Kibana version 6.4.3**

Kibana download: 
https://github.com/ilgwonPark2/SystemAnalysisDesign/wiki/SRS))Kibana

Downloads the three above SWs in your environment.

Please reference the link (github wiki we made)

### Java version upgrade
The ELK Stack of this system is built with Java. Therefore, installing Java version 1.8.0_131 or later is recommended. The JAVA_HOME path is designated to updated Java for use of Elasticsearch.

https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html 

### Git version upgrade
Upgrade git version for the convenience of version management.

https://github.com/ilgwonPark2/SystemAnalysisDesign/wiki/Setting))-git 

### Web
This App shall use Interactor as a Back-end software to host a webpage.

To use this software, it is necessary to require free software license from below link.

https://www.interactor.com/ 

The user can refer the manual for setting http server from below link

https://github.com/ilgwonPark2/SystemAnalysisDesign/wiki/Setting))-Webserver 

## Data Crawling
### Clone the github directory
1. Firstly, clone the github directory via this url: 

      git://github.com/ilgwonPark2/SystemAnalysisDesign.git

2. Before crawling the data, News table should exist in the mysql database. After creating a database with the appropriate name, create a table in mysql with the setted schema.

3. Before executing the python files. You should install some python libraries – BeautifulSoup, selenium and pymysql, chromedriver

4. Then, executing 4 python files in the data_crawling directory (chosun_eng.py, joonang_eng.py, hanGR_eng.py, koreatimes.py).

**+Note: you should change some codes in python files for executing system dynamically.**

1. change the mysql host server address and account

2. change the selenium driver name
(if below codes exist in the python file, current codes are set for Mac OS)

## Data cleansing
### cleansing raw data
Execute python file crawling_cleansing.py on **cd /seoultech/data_cleansing**
+ Delete missing value(article_content).
+ Delete unrelated category contents.
  * Entertainment, Movie, Travel, Lifestyle, Events, art&ent;, food, life
+ Delete Korean contents by regular expression.

## Data Processing
### http request for NLP
1. Before 


