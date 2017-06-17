Android Apps Crawler
====================
Acknowledgement
---------------
This source code is modified from [mssun/android-apps-crawler](https://github.com/mssun/android-apps-crawler)
The REAME is updated with current status
Updates (On going)
------------------
* Updated the Xpath rules defined in settings.py (the original ones don't work any more)
    * Hiapk: http://apk.hiapk.com (hiapk.com)
* Switched to MongoDB for both crawler and downloader
* Modified android_apps_spider.py to use CrawlSpider with rules
    
Overview
--------
Android Apps Crawler is an extensible crawler for downloading Android applications in the third-party markets.
It can crawl the download url addresses of applications and automatically download applications
into repository.

Requirements
------------
* MongoDB
* Python 2.6 or up, not work for python 3
* Scrapy 0.22 or up: http://scrapy.org 
* Works on Linux, Windows, Mac OSX, BSD
* Currently, downloader cannot work on Windows.

File Structure
--------------
```
android-apps-crawler
|   README.md
|   startmongodb.sh
|
|---crawler
|   |   crawl.sh
|   |   scrapy.cfg
|   |  
|---+--android_apps_crawler
|      |   custom_parser.py
|      |   items.py
|      |   middlewares.py
|      |   pipeline.py
|      |   settings.py
|      |   __init__.py
|      |
|      +---spiders
|              android_apps_spider.py 
|
|------<web_site> (used to store the current status for pause/resume)
|
|---downloader
|       downloader.py
+---repo
        apps (store the downloaded APK files)
        databases

```
Usage
-----
* Set the third-party markets you want to crawl in settings.py
* Set the proxy if you have
* start mongoDB manually if needed. DB path is ./repo/database
```
./startmongodb.sh
```
* Start crawler: 
```
./crawler/crawl.sh <market name>
```
* Start downloader:
```
./downloader/downloader.py <database IP:PORT> <DBName:DOCName> <output directory>
```

Settings
--------
You can set proxy, user-agen, database name, etc in ```crawler/android_apps_crawler/settings.py``` file.

Supported Third-party Markets (market names used in crawl.sh)
-----------------------------
* [Invalid] AppChina: http://www.appchina.com (appchina.com)
* Hiapk: http://apk.hiapk.com (hiapk.com)
* [Invalid] Anzhi: http://www.anzhi.com (anzhi.com)
* [Invalid] android.d.cn: http://android.d.cn (android.d.cn)
* [Invalid] mumayi: http://www.mumayi.com (mumayi.com)
* [Invalid] gfan: http://apk.gfan.com (gfan.com)
* [Invalid] nduoa: http://www.nduoa.com (nduoa.com)
* [Invalid] 3gyu: http://www.3gyu.com (3gyu.com)
* [Invalid] angeeks: http://apk.angeeks.com (angeeks.com)
* [Invalid] appfun: http://www.appfun.cn (appfun.cn)
* [Invalid] jimi168: http://www.jimi168.com (jimi168.com)
* Keep adding...

More Android Markets
--------------------
See: https://github.com/mssun/android-markets-list

TODO
----
* Windows support for downloader.
* Crawl apps from shared cloud storage link (e.g, pan.baidu.com, dbank.com).
